<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import * as echarts from 'echarts';
  import type { EChartsOption } from 'echarts';
  import { themeStore } from '../stores/theme';

  export let option: EChartsOption;
  export let height: string = '400px';
  export let loading: boolean = false;

  let chartContainer: HTMLDivElement;
  let chartInstance: echarts.ECharts | null = null;

  // Minimalist color palette for charts
  const lightTheme = {
    color: ['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981'],
    backgroundColor: 'transparent',
    textStyle: {
      color: '#1e293b',
      fontFamily: 'Inter, sans-serif',
    },
    title: {
      textStyle: {
        color: '#1e293b',
        fontWeight: 600,
      },
    },
    line: {
      itemStyle: {
        borderWidth: 2,
      },
      lineStyle: {
        width: 2,
      },
      symbolSize: 6,
      smooth: true,
    },
    axisLine: {
      lineStyle: {
        color: '#e2e8f0',
      },
    },
    splitLine: {
      lineStyle: {
        color: '#f1f5f9',
      },
    },
  };

  const darkTheme = {
    color: ['#60a5fa', '#a78bfa', '#f472b6', '#fbbf24', '#34d399'],
    backgroundColor: 'transparent',
    textStyle: {
      color: '#e2e8f0',
      fontFamily: 'Inter, sans-serif',
    },
    title: {
      textStyle: {
        color: '#f1f5f9',
        fontWeight: 600,
      },
    },
    line: {
      itemStyle: {
        borderWidth: 2,
      },
      lineStyle: {
        width: 2,
      },
      symbolSize: 6,
      smooth: true,
    },
    axisLine: {
      lineStyle: {
        color: '#334155',
      },
    },
    splitLine: {
      lineStyle: {
        color: '#1e293b',
      },
    },
  };

  function initChart() {
    if (!chartContainer) return;

    const isDark = $themeStore.resolvedTheme === 'dark';

    chartInstance = echarts.init(chartContainer, isDark ? darkTheme : lightTheme);
    chartInstance.setOption(option);

    if (loading) {
      chartInstance.showLoading('default', {
        text: 'Loading...',
        color: '#3b82f6',
        textColor: isDark ? '#e2e8f0' : '#1e293b',
        maskColor: isDark ? 'rgba(15, 23, 42, 0.8)' : 'rgba(255, 255, 255, 0.8)',
      });
    }
  }

  function resizeChart() {
    if (chartInstance) {
      chartInstance.resize();
    }
  }

  onMount(() => {
    initChart();
    window.addEventListener('resize', resizeChart);
  });

  onDestroy(() => {
    window.removeEventListener('resize', resizeChart);
    if (chartInstance) {
      chartInstance.dispose();
    }
  });

  // Update chart when option changes
  $: if (chartInstance && option) {
    chartInstance.setOption(option, true);
  }

  // Update chart when loading state changes
  $: if (chartInstance) {
    if (loading) {
      const isDark = $themeStore.resolvedTheme === 'dark';
      chartInstance.showLoading('default', {
        text: 'Loading...',
        color: '#3b82f6',
        textColor: isDark ? '#e2e8f0' : '#1e293b',
        maskColor: isDark ? 'rgba(15, 23, 42, 0.8)' : 'rgba(255, 255, 255, 0.8)',
      });
    } else {
      chartInstance.hideLoading();
    }
  }

  // Reinitialize chart when theme changes
  $: if (chartInstance && $themeStore.resolvedTheme) {
    const isDark = $themeStore.resolvedTheme === 'dark';
    chartInstance.dispose();
    chartInstance = echarts.init(chartContainer, isDark ? darkTheme : lightTheme);
    chartInstance.setOption(option);
  }
</script>

<div bind:this={chartContainer} style="width: 100%; height: {height};"></div>
