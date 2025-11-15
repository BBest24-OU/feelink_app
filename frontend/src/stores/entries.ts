/**
 * Entries store - manages daily log entries
 */
import { writable, derived } from 'svelte/store';
import { entriesApi } from '../lib/api';

export interface EntryValue {
  id: number;
  entry_id: number;
  metric_id: number;
  value_numeric: number | null;
  value_boolean: boolean | null;
  value_text: string | null;
  created_at: string;
}

export interface Entry {
  id: number;
  user_id: number;
  entry_date: string;
  notes: string | null;
  values: EntryValue[];
  created_at: string;
  updated_at: string;
}

interface EntriesState {
  entries: Entry[];
  total: number;
  loading: boolean;
  error: string | null;
}

const initialState: EntriesState = {
  entries: [],
  total: 0,
  loading: false,
  error: null,
};

export const entriesStore = writable<EntriesState>(initialState);

// Derived store - today's entry
export const todayEntry = derived(entriesStore, ($entries) => {
  const today = new Date().toISOString().split('T')[0];
  return $entries.entries.find((e) => e.entry_date === today);
});

// Actions
export const entriesActions = {
  // Load entries with optional filters
  async load(params?: { date_from?: string; date_to?: string; limit?: number; offset?: number }) {
    entriesStore.update((state) => ({ ...state, loading: true, error: null }));

    try {
      const response = await entriesApi.list(params);
      entriesStore.set({
        entries: response.data.entries,
        total: response.data.total,
        loading: false,
        error: null,
      });
      return { success: true };
    } catch (error: any) {
      const errorMsg = error.response?.data?.detail || 'Failed to load entries';
      entriesStore.update((state) => ({ ...state, loading: false, error: errorMsg }));
      return { success: false, error: errorMsg };
    }
  },

  // Create entry
  async create(data: { entry_date: string; notes?: string; values: any[] }) {
    entriesStore.update((state) => ({ ...state, loading: true, error: null }));

    try {
      const response = await entriesApi.create(data);
      entriesStore.update((state) => ({
        ...state,
        entries: [response.data, ...state.entries],
        total: state.total + 1,
        loading: false,
      }));
      return { success: true, data: response.data };
    } catch (error: any) {
      const errorMsg = error.response?.data?.detail || 'Failed to create entry';
      entriesStore.update((state) => ({ ...state, loading: false, error: errorMsg }));
      return { success: false, error: errorMsg };
    }
  },

  // Update entry
  async update(id: number, data: { notes?: string; values?: any[] }) {
    entriesStore.update((state) => ({ ...state, loading: true, error: null }));

    try {
      const response = await entriesApi.update(id, data);
      entriesStore.update((state) => ({
        ...state,
        entries: state.entries.map((e) => (e.id === id ? response.data : e)),
        loading: false,
      }));
      return { success: true };
    } catch (error: any) {
      const errorMsg = error.response?.data?.detail || 'Failed to update entry';
      entriesStore.update((state) => ({ ...state, loading: false, error: errorMsg }));
      return { success: false, error: errorMsg };
    }
  },

  // Delete entry
  async delete(id: number) {
    try {
      await entriesApi.delete(id);
      entriesStore.update((state) => ({
        ...state,
        entries: state.entries.filter((e) => e.id !== id),
        total: state.total - 1,
      }));
      return { success: true };
    } catch (error: any) {
      return { success: false, error: error.response?.data?.detail };
    }
  },

  // Get entry by date
  async getByDate(date: string) {
    try {
      const response = await entriesApi.getByDate(date);
      return { success: true, data: response.data };
    } catch (error: any) {
      if (error.response?.status === 404) {
        return { success: true, data: null };
      }
      return { success: false, error: error.response?.data?.detail };
    }
  },
};
