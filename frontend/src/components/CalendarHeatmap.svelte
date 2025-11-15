<script lang="ts">
  import type { Entry } from '../stores/entries';
  import { format, startOfMonth, endOfMonth, eachDayOfInterval, isSameDay, addMonths, subMonths } from 'date-fns';

  export let entries: Entry[] = [];
  export let onDateClick: (date: string) => void = () => {};

  let currentMonth = new Date();

  $: monthStart = startOfMonth(currentMonth);
  $: monthEnd = endOfMonth(currentMonth);
  $: daysInMonth = eachDayOfInterval({ start: monthStart, end: monthEnd });

  // Get day of week for the first day (0 = Sunday, 1 = Monday, etc.)
  $: firstDayOfWeek = monthStart.getDay();

  // Create entry date set for quick lookup
  $: entryDates = new Set(entries.map((e) => e.entry_date));

  // Get entry count for a date
  function getEntryStatus(date: Date): 'complete' | 'partial' | 'none' {
    const dateStr = format(date, 'yyyy-MM-dd');
    if (!entryDates.has(dateStr)) return 'none';

    const entry = entries.find((e) => e.entry_date === dateStr);
    if (!entry) return 'none';

    // Consider complete if has at least one value
    return entry.values.length > 0 ? 'complete' : 'partial';
  }

  function handleDateClick(date: Date) {
    const dateStr = format(date, 'yyyy-MM-dd');
    onDateClick(dateStr);
  }

  function previousMonth() {
    currentMonth = subMonths(currentMonth, 1);
  }

  function nextMonth() {
    currentMonth = addMonths(currentMonth, 1);
  }

  function isToday(date: Date): boolean {
    return isSameDay(date, new Date());
  }
</script>

<div class="calendar-heatmap">
  <div class="calendar-header">
    <button on:click={previousMonth} class="nav-button">←</button>
    <h3 class="month-title">{format(currentMonth, 'MMMM yyyy')}</h3>
    <button on:click={nextMonth} class="nav-button">→</button>
  </div>

  <div class="calendar-grid">
    <!-- Day headers -->
    {#each ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'] as day}
      <div class="day-header">{day}</div>
    {/each}

    <!-- Empty cells for days before month starts -->
    {#each Array(firstDayOfWeek) as _}
      <div class="calendar-day empty"></div>
    {/each}

    <!-- Days of month -->
    {#each daysInMonth as day}
      {@const status = getEntryStatus(day)}
      {@const today = isToday(day)}
      <button
        class="calendar-day"
        class:has-entry={status !== 'none'}
        class:complete={status === 'complete'}
        class:partial={status === 'partial'}
        class:today={today}
        on:click={() => handleDateClick(day)}
      >
        <span class="day-number">{format(day, 'd')}</span>
      </button>
    {/each}
  </div>

  <div class="legend">
    <span class="legend-item">
      <span class="legend-box none"></span>
      <span>No entry</span>
    </span>
    <span class="legend-item">
      <span class="legend-box partial"></span>
      <span>Partial</span>
    </span>
    <span class="legend-item">
      <span class="legend-box complete"></span>
      <span>Complete</span>
    </span>
  </div>
</div>

<style>
  .calendar-heatmap {
    width: 100%;
  }

  .calendar-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
  }

  .month-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: #1f2937;
  }

  .nav-button {
    padding: 0.5rem 1rem;
    background-color: #f3f4f6;
    border: none;
    border-radius: 0.375rem;
    cursor: pointer;
    font-size: 1.25rem;
    color: #4b5563;
    transition: background-color 0.2s;
  }

  .nav-button:hover {
    background-color: #e5e7eb;
  }

  .calendar-grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 0.5rem;
  }

  .day-header {
    text-align: center;
    font-size: 0.875rem;
    font-weight: 600;
    color: #6b7280;
    padding: 0.5rem;
  }

  .calendar-day {
    aspect-ratio: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid #e5e7eb;
    border-radius: 0.375rem;
    background-color: #fff;
    cursor: pointer;
    transition: all 0.2s;
  }

  .calendar-day.empty {
    background-color: transparent;
    border: none;
    cursor: default;
  }

  .calendar-day:not(.empty):hover {
    transform: scale(1.05);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .calendar-day.complete {
    background-color: #10b981;
    color: white;
    border-color: #059669;
  }

  .calendar-day.partial {
    background-color: #fbbf24;
    color: white;
    border-color: #f59e0b;
  }

  .calendar-day.today {
    border: 2px solid #3b82f6;
    font-weight: 700;
  }

  .day-number {
    font-size: 0.875rem;
  }

  .legend {
    display: flex;
    justify-content: center;
    gap: 1.5rem;
    margin-top: 1.5rem;
    font-size: 0.875rem;
    color: #6b7280;
  }

  .legend-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .legend-box {
    width: 1rem;
    height: 1rem;
    border-radius: 0.25rem;
    border: 1px solid #e5e7eb;
  }

  .legend-box.none {
    background-color: #fff;
  }

  .legend-box.partial {
    background-color: #fbbf24;
  }

  .legend-box.complete {
    background-color: #10b981;
  }
</style>
