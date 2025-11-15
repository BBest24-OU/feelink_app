<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import {
    Chart,
    LineController,
    LineElement,
    PointElement,
    LinearScale,
    TimeScale,
    Title,
    Tooltip,
    Legend,
    CategoryScale,
    type ChartConfiguration,
  } from 'chart.js';
  import 'chartjs-adapter-date-fns';

  // Register Chart.js components
  Chart.register(
    LineController,
    LineElement,
    PointElement,
    LinearScale,
    TimeScale,
    CategoryScale,
    Title,
    Tooltip,
    Legend
  );

  export let title: string = '';
  export let datasets: Array<{
    label: string;
    data: Array<{ x: string | Date; y: number }>;
    borderColor?: string;
    backgroundColor?: string;
  }> = [];
  export let height: number = 300;
  export let xAxisType: 'time' | 'category' = 'time';

  let canvas: HTMLCanvasElement;
  let chart: Chart | null = null;

  onMount(() => {
    if (!canvas) return;

    const config: ChartConfiguration = {
      type: 'line',
      data: {
        datasets: datasets.map((ds, index) => ({
          label: ds.label,
          data: ds.data,
          borderColor: ds.borderColor || `hsl(${index * 60}, 70%, 50%)`,
          backgroundColor: ds.backgroundColor || `hsla(${index * 60}, 70%, 50%, 0.1)`,
          tension: 0.3,
          fill: true,
          pointRadius: 4,
          pointHoverRadius: 6,
        })),
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: !!title,
            text: title,
            font: {
              size: 16,
              weight: 'bold',
            },
          },
          tooltip: {
            mode: 'index',
            intersect: false,
          },
          legend: {
            display: datasets.length > 1,
            position: 'top',
          },
        },
        scales: {
          x: {
            type: xAxisType,
            title: {
              display: true,
              text: 'Date',
            },
            ...(xAxisType === 'time' && {
              time: {
                unit: 'day',
                displayFormats: {
                  day: 'MMM d',
                },
              },
            }),
          },
          y: {
            title: {
              display: true,
              text: 'Value',
            },
            beginAtZero: false,
          },
        },
        interaction: {
          mode: 'nearest',
          axis: 'x',
          intersect: false,
        },
      },
    };

    chart = new Chart(canvas, config);
  });

  onDestroy(() => {
    if (chart) {
      chart.destroy();
      chart = null;
    }
  });

  // Update chart when datasets change
  $: if (chart && datasets) {
    chart.data.datasets = datasets.map((ds, index) => ({
      label: ds.label,
      data: ds.data,
      borderColor: ds.borderColor || `hsl(${index * 60}, 70%, 50%)`,
      backgroundColor: ds.backgroundColor || `hsla(${index * 60}, 70%, 50%, 0.1)`,
      tension: 0.3,
      fill: true,
      pointRadius: 4,
      pointHoverRadius: 6,
    }));
    chart.update();
  }
</script>

<div class="chart-container" style="height: {height}px;">
  <canvas bind:this={canvas}></canvas>
</div>

<style>
  .chart-container {
    position: relative;
    width: 100%;
  }
</style>
