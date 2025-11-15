<script lang="ts">
  export let correlations: Array<{
    metric_1_name: string;
    metric_2_name: string;
    coefficient: float;
    significant: boolean;
  }> = [];

  // Get unique metric names
  $: metricNames = Array.from(
    new Set([
      ...correlations.map(c => c.metric_1_name),
      ...correlations.map(c => c.metric_2_name)
    ])
  ).sort();

  // Build matrix
  $: matrix = (() => {
    const mat: Record<string, Record<string, { coefficient: number; significant: boolean } | null>> = {};

    // Initialize matrix
    metricNames.forEach(name1 => {
      mat[name1] = {};
      metricNames.forEach(name2 => {
        mat[name1][name2] = null;
      });
    });

    // Fill matrix with correlation data
    correlations.forEach(corr => {
      mat[corr.metric_1_name][corr.metric_2_name] = {
        coefficient: corr.coefficient,
        significant: corr.significant
      };
      mat[corr.metric_2_name][corr.metric_1_name] = {
        coefficient: corr.coefficient,
        significant: corr.significant
      };
    });

    // Diagonal is always 1.0
    metricNames.forEach(name => {
      mat[name][name] = { coefficient: 1.0, significant: true };
    });

    return mat;
  })();

  function getColor(coefficient: number | null): string {
    if (coefficient === null) return 'bg-gray-100';

    const abs = Math.abs(coefficient);

    if (coefficient > 0) {
      // Positive correlation - blue shades
      if (abs >= 0.7) return 'bg-blue-700';
      if (abs >= 0.5) return 'bg-blue-500';
      if (abs >= 0.3) return 'bg-blue-300';
      return 'bg-blue-100';
    } else {
      // Negative correlation - red shades
      if (abs >= 0.7) return 'bg-red-700';
      if (abs >= 0.5) return 'bg-red-500';
      if (abs >= 0.3) return 'bg-red-300';
      return 'bg-red-100';
    }
  }

  function getTextColor(coefficient: number | null): string {
    if (coefficient === null) return 'text-gray-400';

    const abs = Math.abs(coefficient);
    return abs >= 0.5 ? 'text-white' : 'text-gray-800';
  }
</script>

{#if metricNames.length === 0}
  <div class="text-center py-8 text-gray-500">
    No correlation data available
  </div>
{:else}
  <div class="overflow-x-auto">
    <div class="inline-block min-w-full">
      <div class="grid gap-1" style="grid-template-columns: 150px repeat({metricNames.length}, 80px);">
        <!-- Top left corner -->
        <div></div>

        <!-- Column headers -->
        {#each metricNames as name}
          <div class="text-xs font-medium text-gray-700 transform -rotate-45 origin-bottom-left h-20 flex items-end justify-start pl-2">
            <span class="whitespace-nowrap">{name}</span>
          </div>
        {/each}

        <!-- Matrix rows -->
        {#each metricNames as rowName, i}
          <!-- Row header -->
          <div class="text-xs font-medium text-gray-700 flex items-center pr-2 text-right">
            {rowName}
          </div>

          <!-- Matrix cells -->
          {#each metricNames as colName, j}
            {@const cell = matrix[rowName][colName]}
            <div
              class="h-20 flex items-center justify-center text-xs font-medium {getColor(cell?.coefficient ?? null)} {getTextColor(cell?.coefficient ?? null)} border border-gray-200 cursor-pointer hover:opacity-80 transition-opacity"
              title="{rowName} × {colName}: {cell?.coefficient?.toFixed(2) ?? 'N/A'}"
            >
              {#if cell !== null}
                <span>
                  {cell.coefficient.toFixed(2)}
                  {#if !cell.significant}
                    <span class="text-xs">*</span>
                  {/if}
                </span>
              {:else}
                <span>—</span>
              {/if}
            </div>
          {/each}
        {/each}
      </div>

      <!-- Legend -->
      <div class="mt-6 flex flex-wrap gap-4 text-sm">
        <div class="flex items-center gap-2">
          <div class="w-8 h-4 bg-blue-700"></div>
          <span>Strong positive</span>
        </div>
        <div class="flex items-center gap-2">
          <div class="w-8 h-4 bg-blue-300"></div>
          <span>Weak positive</span>
        </div>
        <div class="flex items-center gap-2">
          <div class="w-8 h-4 bg-gray-100"></div>
          <span>No data</span>
        </div>
        <div class="flex items-center gap-2">
          <div class="w-8 h-4 bg-red-300"></div>
          <span>Weak negative</span>
        </div>
        <div class="flex items-center gap-2">
          <div class="w-8 h-4 bg-red-700"></div>
          <span>Strong negative</span>
        </div>
        <div class="text-gray-600">
          * = not statistically significant
        </div>
      </div>
    </div>
  </div>
{/if}
