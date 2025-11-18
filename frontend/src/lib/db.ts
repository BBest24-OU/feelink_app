import Dexie, { type Table } from 'dexie';

// Database interfaces
export interface DBMetric {
  id: number;
  user_id: number;
  name_key: string;
  category: string;
  value_type: string;
  min_value?: number;
  max_value?: number;
  color?: string;
  icon?: string;
  display_order: number;
  archived: boolean;
  created_at: string;
  updated_at: string;
}

export interface DBEntry {
  id: number;
  user_id: number;
  entry_date: string;
  notes?: string;
  values: DBEntryValue[];
  created_at: string;
  updated_at: string;
}

export interface DBEntryValue {
  id: number;
  entry_id: number;
  metric_id: number;
  value_numeric?: number;
  value_boolean?: boolean;
  value_text?: string;
  created_at: string;
}

export interface SyncOperation {
  id?: number;
  operation: 'CREATE' | 'UPDATE' | 'DELETE';
  entity: 'metric' | 'entry' | 'user';
  entity_id?: number;
  data: any;
  timestamp: number;
  retry_count: number;
  status: 'pending' | 'processing' | 'failed';
  error?: string;
}

export interface UserSettings {
  key: string;
  value: any;
  updated_at: number;
}

// Dexie database class
export class FeelinkDB extends Dexie {
  metrics!: Table<DBMetric, number>;
  entries!: Table<DBEntry, number>;
  syncQueue!: Table<SyncOperation, number>;
  userSettings!: Table<UserSettings, string>;

  constructor() {
    super('FeelinkDB');

    this.version(1).stores({
      metrics: 'id, user_id, category, archived, display_order',
      entries: 'id, user_id, entry_date, created_at',
      syncQueue: '++id, status, timestamp, entity',
      userSettings: 'key'
    });
  }
}

// Create and export database instance
export const db = new FeelinkDB();

// Database helper functions
export const dbHelpers = {
  // Metrics
  async getAllMetrics(): Promise<DBMetric[]> {
    return await db.metrics.toArray();
  },

  async getActiveMetrics(): Promise<DBMetric[]> {
    // Use filter instead of where().equals() to avoid WeakMap issues with boolean values
    const allMetrics = await db.metrics.toArray();
    return allMetrics.filter((m: DBMetric) => !m.archived);
  },

  async getMetricById(id: number): Promise<DBMetric | undefined> {
    return await db.metrics.get(id);
  },

  async saveMetric(metric: DBMetric): Promise<number> {
    return await db.metrics.put(metric);
  },

  async saveMetrics(metrics: DBMetric[]): Promise<void> {
    await db.metrics.bulkPut(metrics);
  },

  async deleteMetric(id: number): Promise<void> {
    await db.metrics.delete(id);
  },

  async clearMetrics(): Promise<void> {
    await db.metrics.clear();
  },

  // Entries
  async getAllEntries(): Promise<DBEntry[]> {
    return await db.entries.orderBy('entry_date').reverse().toArray();
  },

  async getEntriesByDateRange(from: string, to: string): Promise<DBEntry[]> {
    return await db.entries
      .where('entry_date')
      .between(from, to, true, true)
      .reverse()
      .toArray();
  },

  async getEntryByDate(date: string): Promise<DBEntry | undefined> {
    return await db.entries.where('entry_date').equals(date).first();
  },

  async getEntryById(id: number): Promise<DBEntry | undefined> {
    return await db.entries.get(id);
  },

  async saveEntry(entry: DBEntry): Promise<number> {
    return await db.entries.put(entry);
  },

  async saveEntries(entries: DBEntry[]): Promise<void> {
    await db.entries.bulkPut(entries);
  },

  async deleteEntry(id: number): Promise<void> {
    await db.entries.delete(id);
  },

  async clearEntries(): Promise<void> {
    await db.entries.clear();
  },

  // Sync Queue
  async addToSyncQueue(operation: Omit<SyncOperation, 'id'>): Promise<number> {
    return await db.syncQueue.add(operation as SyncOperation);
  },

  async getPendingSyncOperations(): Promise<SyncOperation[]> {
    return await db.syncQueue
      .where('status')
      .equals('pending')
      .sortBy('timestamp');
  },

  async updateSyncOperation(id: number, updates: Partial<SyncOperation>): Promise<void> {
    await db.syncQueue.update(id, updates);
  },

  async deleteSyncOperation(id: number): Promise<void> {
    await db.syncQueue.delete(id);
  },

  async clearSyncQueue(): Promise<void> {
    await db.syncQueue.clear();
  },

  // User Settings
  async getSetting(key: string): Promise<any> {
    const setting = await db.userSettings.get(key);
    return setting?.value;
  },

  async saveSetting(key: string, value: any): Promise<void> {
    await db.userSettings.put({
      key,
      value,
      updated_at: Date.now()
    });
  },

  async deleteSetting(key: string): Promise<void> {
    await db.userSettings.delete(key);
  },

  // General
  async clearAllData(): Promise<void> {
    await db.metrics.clear();
    await db.entries.clear();
    await db.syncQueue.clear();
    await db.userSettings.clear();
  }
};
