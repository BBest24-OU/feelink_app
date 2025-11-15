/**
 * Metrics store - manages user metrics
 */
import { writable, derived } from 'svelte/store';
import { metricsApi } from '../lib/api';

export interface Metric {
  id: number;
  user_id: number;
  name_key: string;
  category: string;
  value_type: string;
  min_value: number | null;
  max_value: number | null;
  description: string | null;
  color: string | null;
  icon: string | null;
  display_order: number;
  archived: boolean;
  created_at: string;
  updated_at: string;
}

interface MetricsState {
  metrics: Metric[];
  loading: boolean;
  error: string | null;
}

const initialState: MetricsState = {
  metrics: [],
  loading: false,
  error: null,
};

export const metricsStore = writable<MetricsState>(initialState);

// Derived stores
export const activeMetrics = derived(metricsStore, ($metrics) =>
  $metrics.metrics.filter((m) => !m.archived)
);

export const metricsByCategory = derived(activeMetrics, ($metrics) => {
  const grouped: Record<string, Metric[]> = {};
  $metrics.forEach((metric) => {
    if (!grouped[metric.category]) {
      grouped[metric.category] = [];
    }
    grouped[metric.category].push(metric);
  });
  return grouped;
});

// Actions
export const metricsActions = {
  // Load all metrics
  async load(includeArchived: boolean = false) {
    metricsStore.update((state) => ({ ...state, loading: true, error: null }));

    try {
      const response = await metricsApi.list(includeArchived);
      metricsStore.set({
        metrics: response.data.metrics,
        loading: false,
        error: null,
      });
      return { success: true };
    } catch (error: any) {
      const errorMsg = error.response?.data?.detail || 'Failed to load metrics';
      metricsStore.update((state) => ({ ...state, loading: false, error: errorMsg }));
      return { success: false, error: errorMsg };
    }
  },

  // Create metric
  async create(data: any) {
    metricsStore.update((state) => ({ ...state, loading: true, error: null }));

    try {
      const response = await metricsApi.create(data);
      metricsStore.update((state) => ({
        ...state,
        metrics: [...state.metrics, response.data],
        loading: false,
      }));
      return { success: true, data: response.data };
    } catch (error: any) {
      const errorMsg = error.response?.data?.detail || 'Failed to create metric';
      metricsStore.update((state) => ({ ...state, loading: false, error: errorMsg }));
      return { success: false, error: errorMsg };
    }
  },

  // Update metric
  async update(id: number, data: any) {
    metricsStore.update((state) => ({ ...state, loading: true, error: null }));

    try {
      const response = await metricsApi.update(id, data);
      metricsStore.update((state) => ({
        ...state,
        metrics: state.metrics.map((m) => (m.id === id ? response.data : m)),
        loading: false,
      }));
      return { success: true };
    } catch (error: any) {
      const errorMsg = error.response?.data?.detail || 'Failed to update metric';
      metricsStore.update((state) => ({ ...state, loading: false, error: errorMsg }));
      return { success: false, error: errorMsg };
    }
  },

  // Archive metric
  async archive(id: number) {
    try {
      await metricsApi.archive(id);
      metricsStore.update((state) => ({
        ...state,
        metrics: state.metrics.map((m) => (m.id === id ? { ...m, archived: true } : m)),
      }));
      return { success: true };
    } catch (error: any) {
      return { success: false, error: error.response?.data?.detail };
    }
  },

  // Unarchive metric
  async unarchive(id: number) {
    try {
      const response = await metricsApi.unarchive(id);
      metricsStore.update((state) => ({
        ...state,
        metrics: state.metrics.map((m) => (m.id === id ? response.data : m)),
      }));
      return { success: true };
    } catch (error: any) {
      return { success: false, error: error.response?.data?.detail };
    }
  },
};
