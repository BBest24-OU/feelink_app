<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import {
    Chart,
    ScatterController,
    PointElement,
    LinearScale,
    Title,
    Tooltip,
    Legend,
    type ChartConfiguration,
  } from 'chart.js';

  // Register Chart.js components
  Chart.register(
    ScatterController,
    PointElement,
    LinearScale,
    Title,
    Tooltip,
    Legend
  );

  export let title: string = '';
  export let xLabel: string = 'X';
  export let yLabel: string = 'Y';
  export let data: Array<{ x: number; y: number }> = [];
  export let coefficient: number | null = null;
  export let height: number = 400;

  let canvas: HTMLCanvasElement;
  let chart: Chart | null = null;

  onMount(() => {
    if (!canvas) return;

    const config: ChartConfiguration = {
      type: 'scatter',
      data: {
        datasets: [
          {
            label: `${xLabel} vs ${yLabel}`,
            data,
            backgroundColor: 'rgba(59, 130, 246, 0.6)',
            borderColor: 'rgba(59, 130, 246, 1)',
            pointRadius: 6,
            pointHoverRadius: 8,
          },
        ],
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
            callbacks: {
              label: function (context) {
                const point = context.parsed;
                let label = `${xLabel}: ${point.x.toFixed(2)}, ${yLabel}: ${point.y.toFixed(2)}`;
                if (coefficient !== null) {
                  label += ` | r=${coefficient.toFixed(3)}`;
                }
                return label;
              },
            },
          },
          legend: {
            display: false,
          },
        },
        scales: {
          x: {
            title: {
              display: true,
              text: xLabel,
              font: {
                size: 14,
                weight: 'bold',
              },
            },
            ticks: {
              precision: 1,
            },
          },
          y: {
            title: {
              display: true,
              text: yLabel,
              font: {
                size: 14,
                weight: 'bold',
              },
            },
            ticks: {
              precision: 1,
            },
          },
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

  // Update chart when data changes
  $: if (chart && data) {
    chart.data.datasets[0].data = data;
    chart.update();
  }
</script>

<div class="scatter-plot-container" style="height: {height}px;">
  <canvas bind:this={canvas}></canvas>

  {#if coefficient !== null}
    <div class="mt-2 text-center text-sm text-gray-600">
      Correlation coefficient: <span class="font-semibold">{coefficient.toFixed(3)}</span>
      {#if Math.abs(coefficient) >= 0.7}
        <span class="text-blue-600">(Strong)</span>
      {:else if Math.abs(coefficient) >= 0.3}
        <span class="text-yellow-600">(Moderate)</span>
      {:else}
        <span class="text-gray-500">(Weak)</span>
      {/if}
    </div>
  {/if}
</div>

<style>
  .scatter-plot-container {
    position: relative;
    width: 100%;
  }
</style>
