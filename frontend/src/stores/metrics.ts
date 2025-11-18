/**
 * Metrics store - manages user metrics with offline support
 */
import { writable, derived } from 'svelte/store';
import { metricsApi } from '../lib/api';
import { dbHelpers } from '../lib/db';
import { syncActions } from '../lib/sync';

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
  // Load all metrics (offline-first)
  async load(includeArchived: boolean = false) {
    metricsStore.update((state) => ({ ...state, loading: true, error: null }));

    try {
      // Try to load from IndexedDB first
      const cachedMetrics = includeArchived
        ? await dbHelpers.getAllMetrics()
        : await dbHelpers.getActiveMetrics();

      if (cachedMetrics.length > 0) {
        metricsStore.update((state) => ({
          ...state,
          metrics: cachedMetrics as Metric[],
          loading: false,
        }));
      }

      // If online, fetch from API and update cache
      if (navigator.onLine) {
        const response = await metricsApi.list(includeArchived);
        const metrics = response.data.metrics;

        // Update IndexedDB
        await dbHelpers.clearMetrics();
        await dbHelpers.saveMetrics(metrics);

        metricsStore.set({
          metrics,
          loading: false,
          error: null,
        });
      } else if (cachedMetrics.length === 0) {
        metricsStore.update((state) => ({
          ...state,
          loading: false,
          error: 'No cached data and offline',
        }));
      }

      return { success: true };
    } catch (error: any) {
      const errorMsg = error.response?.data?.detail || 'Failed to load metrics';
      metricsStore.update((state) => ({ ...state, loading: false, error: errorMsg }));
      return { success: false, error: errorMsg };
    }
  },

  // Create metric (offline-supported)
  async create(data: any) {
    metricsStore.update((state) => ({ ...state, loading: true, error: null }));

    try {
      if (navigator.onLine) {
        const response = await metricsApi.create(data);
        const metric = response.data;

        // Update IndexedDB
        await dbHelpers.saveMetric(metric);

        metricsStore.update((state) => ({
          ...state,
          metrics: [...state.metrics, metric],
          loading: false,
        }));
        return { success: true, data: metric };
      } else {
        // Offline: create temporary ID and add to sync queue
        const tempMetric = {
          ...data,
          id: -Date.now(), // Temporary negative ID
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
        };

        await dbHelpers.saveMetric(tempMetric);
        await syncActions.addToQueue('CREATE', 'metric', data);

        metricsStore.update((state) => ({
          ...state,
          metrics: [...state.metrics, tempMetric],
          loading: false,
        }));
        return { success: true, data: tempMetric };
      }
    } catch (error: any) {
      const errorMsg = error.response?.data?.detail || 'Failed to create metric';
      metricsStore.update((state) => ({ ...state, loading: false, error: errorMsg }));
      return { success: false, error: errorMsg };
    }
  },

  // Update metric (offline-supported)
  async update(id: number, data: any) {
    metricsStore.update((state) => ({ ...state, loading: true, error: null }));

    try {
      if (navigator.onLine) {
        const response = await metricsApi.update(id, data);
        const metric = response.data;

        // Update IndexedDB
        await dbHelpers.saveMetric(metric);

        metricsStore.update((state) => ({
          ...state,
          metrics: state.metrics.map((m) => (m.id === id ? metric : m)),
          loading: false,
        }));
        return { success: true };
      } else {
        // Offline: update local data and queue sync
        const updatedMetric = await dbHelpers.getMetricById(id);
        if (updatedMetric) {
          const newMetric = { ...updatedMetric, ...data, updated_at: new Date().toISOString() };
          await dbHelpers.saveMetric(newMetric);
          await syncActions.addToQueue('UPDATE', 'metric', data, id);

          metricsStore.update((state) => ({
            ...state,
            metrics: state.metrics.map((m) => (m.id === id ? newMetric as Metric : m)),
            loading: false,
          }));
        }
        return { success: true };
      }
    } catch (error: any) {
      const errorMsg = error.response?.data?.detail || 'Failed to update metric';
      metricsStore.update((state) => ({ ...state, loading: false, error: errorMsg }));
      return { success: false, error: errorMsg };
    }
  },

  // Archive metric (offline-supported)
  async archive(id: number) {
    try {
      const metric = await dbHelpers.getMetricById(id);
      if (!metric) return { success: false, error: 'Metric not found' };

      const updated = { ...metric, archived: true };

      if (navigator.onLine) {
        await metricsApi.archive(id);
      } else {
        await syncActions.addToQueue('UPDATE', 'metric', { archived: true }, id);
      }

      await dbHelpers.saveMetric(updated as any);
      metricsStore.update((state) => ({
        ...state,
        metrics: state.metrics.map((m) => (m.id === id ? updated as Metric : m)),
      }));
      return { success: true };
    } catch (error: any) {
      return { success: false, error: error.response?.data?.detail };
    }
  },

  // Unarchive metric (offline-supported)
  async unarchive(id: number) {
    try {
      let metric;

      if (navigator.onLine) {
        const response = await metricsApi.unarchive(id);
        metric = response.data;
        await dbHelpers.saveMetric(metric);
      } else {
        const cached = await dbHelpers.getMetricById(id);
        if (!cached) return { success: false, error: 'Metric not found' };
        metric = { ...cached, archived: false };
        await dbHelpers.saveMetric(metric as any);
        await syncActions.addToQueue('UPDATE', 'metric', { archived: false }, id);
      }

      metricsStore.update((state) => ({
        ...state,
        metrics: state.metrics.map((m) => (m.id === id ? metric as Metric : m)),
      }));
      return { success: true };
    } catch (error: any) {
      return { success: false, error: error.response?.data?.detail };
    }
  },
};
