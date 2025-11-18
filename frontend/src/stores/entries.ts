/**
 * Entries store - manages daily log entries with offline support
 */
import { writable, derived } from 'svelte/store';
import { entriesApi } from '../lib/api';
import { dbHelpers } from '../lib/db';
import { syncActions } from '../lib/sync';

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
  // Load entries with optional filters (offline-first)
  async load(params?: { date_from?: string; date_to?: string; limit?: number; offset?: number }) {
    entriesStore.update((state) => ({ ...state, loading: true, error: null }));

    try {
      // Try to load from IndexedDB first
      let cachedEntries;
      if (params?.date_from && params?.date_to) {
        cachedEntries = await dbHelpers.getEntriesByDateRange(params.date_from, params.date_to);
      } else {
        cachedEntries = await dbHelpers.getAllEntries();
      }

      if (cachedEntries.length > 0) {
        entriesStore.update((state) => ({
          ...state,
          entries: cachedEntries as Entry[],
          total: cachedEntries.length,
          loading: false,
        }));
      }

      // If online, fetch from API and update cache
      if (navigator.onLine) {
        const response = await entriesApi.list(params);
        const entries = response.data.entries;

        // Update IndexedDB
        await dbHelpers.clearEntries();
        await dbHelpers.saveEntries(entries);

        entriesStore.set({
          entries,
          total: response.data.total,
          loading: false,
          error: null,
        });
      } else if (cachedEntries.length === 0) {
        entriesStore.update((state) => ({
          ...state,
          loading: false,
          error: 'No cached data and offline',
        }));
      }

      return { success: true };
    } catch (error: any) {
      const errorMsg = error.response?.data?.detail || 'Failed to load entries';
      entriesStore.update((state) => ({ ...state, loading: false, error: errorMsg }));
      return { success: false, error: errorMsg };
    }
  },

  // Create entry (offline-supported)
  async create(data: { entry_date: string; notes?: string; values: any[] }) {
    entriesStore.update((state) => ({ ...state, loading: true, error: null }));

    try {
      if (navigator.onLine) {
        const response = await entriesApi.create(data);
        const entry = response.data;

        // Update IndexedDB
        await dbHelpers.saveEntry(entry);

        entriesStore.update((state) => ({
          ...state,
          entries: [entry, ...state.entries],
          total: state.total + 1,
          loading: false,
        }));
        return { success: true, data: entry };
      } else {
        // Offline: create temporary ID and add to sync queue
        const tempEntry = {
          ...data,
          id: -Date.now(),
          user_id: 0, // Will be set by server
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
        };

        await dbHelpers.saveEntry(tempEntry);
        await syncActions.addToQueue('CREATE', 'entry', data);

        entriesStore.update((state) => ({
          ...state,
          entries: [tempEntry, ...state.entries],
          total: state.total + 1,
          loading: false,
        }));
        return { success: true, data: tempEntry };
      }
    } catch (error: any) {
      const errorMsg = error.response?.data?.detail || 'Failed to create entry';
      entriesStore.update((state) => ({ ...state, loading: false, error: errorMsg }));
      return { success: false, error: errorMsg };
    }
  },

  // Update entry (offline-supported)
  async update(id: number, data: { notes?: string; values?: any[] }) {
    entriesStore.update((state) => ({ ...state, loading: true, error: null }));

    try {
      if (navigator.onLine) {
        const response = await entriesApi.update(id, data);
        const entry = response.data;

        // Update IndexedDB
        await dbHelpers.saveEntry(entry);

        entriesStore.update((state) => ({
          ...state,
          entries: state.entries.map((e) => (e.id === id ? entry : e)),
          loading: false,
        }));
        return { success: true };
      } else {
        // Offline: update local data and queue sync
        const existingEntry = await dbHelpers.getEntryById(id);
        if (existingEntry) {
          const updated = { ...existingEntry, ...data, updated_at: new Date().toISOString() };
          await dbHelpers.saveEntry(updated as any);
          await syncActions.addToQueue('UPDATE', 'entry', data, id);

          entriesStore.update((state) => ({
            ...state,
            entries: state.entries.map((e) => (e.id === id ? updated as Entry : e)),
            loading: false,
          }));
        }
        return { success: true };
      }
    } catch (error: any) {
      const errorMsg = error.response?.data?.detail || 'Failed to update entry';
      entriesStore.update((state) => ({ ...state, loading: false, error: errorMsg }));
      return { success: false, error: errorMsg };
    }
  },

  // Delete entry (offline-supported)
  async delete(id: number) {
    try {
      if (navigator.onLine) {
        await entriesApi.delete(id);
      } else {
        await syncActions.addToQueue('DELETE', 'entry', {}, id);
      }

      await dbHelpers.deleteEntry(id);
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
