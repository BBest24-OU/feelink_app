/**
 * Unit tests for database helpers
 */
import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { db, dbHelpers } from './db';
import type { DBMetric, DBEntry } from './db';

describe('Database Helpers', () => {
  beforeEach(async () => {
    // Clear database before each test
    await db.metrics.clear();
    await db.entries.clear();
    await db.syncQueue.clear();
    await db.userSettings.clear();
  });

  afterEach(async () => {
    // Clean up after each test
    await db.metrics.clear();
    await db.entries.clear();
    await db.syncQueue.clear();
    await db.userSettings.clear();
  });

  describe('Metrics', () => {
    it('should save metrics to database', async () => {
      const metrics: DBMetric[] = [
        {
          id: 1,
          user_id: 1,
          name_key: 'metric.sleep',
          category: 'physical',
          value_type: 'numeric',
          unit: 'hours',
          archived: false,
          display_order: 1,
        },
      ];

      await dbHelpers.saveMetrics(metrics);

      const saved = await db.metrics.toArray();
      expect(saved).toHaveLength(1);
      expect(saved[0].name_key).toBe('metric.sleep');
    });

    it('should get all metrics', async () => {
      const metrics: DBMetric[] = [
        {
          id: 1,
          user_id: 1,
          name_key: 'metric.sleep',
          category: 'physical',
          value_type: 'numeric',
          archived: false,
          display_order: 1,
        },
        {
          id: 2,
          user_id: 1,
          name_key: 'metric.mood',
          category: 'mental',
          value_type: 'numeric',
          archived: false,
          display_order: 2,
        },
      ];

      await dbHelpers.saveMetrics(metrics);

      const all = await dbHelpers.getAllMetrics();
      expect(all).toHaveLength(2);
    });

    it('should get only active metrics', async () => {
      const metrics: DBMetric[] = [
        {
          id: 1,
          user_id: 1,
          name_key: 'metric.sleep',
          category: 'physical',
          value_type: 'numeric',
          archived: false,
          display_order: 1,
        },
        {
          id: 2,
          user_id: 1,
          name_key: 'metric.archived',
          category: 'mental',
          value_type: 'numeric',
          archived: true,
          display_order: 2,
        },
      ];

      await dbHelpers.saveMetrics(metrics);

      const active = await dbHelpers.getActiveMetrics();
      expect(active).toHaveLength(1);
      expect(active[0].name_key).toBe('metric.sleep');
    });

    it('should clear all metrics', async () => {
      const metrics: DBMetric[] = [
        {
          id: 1,
          user_id: 1,
          name_key: 'metric.sleep',
          category: 'physical',
          value_type: 'numeric',
          archived: false,
          display_order: 1,
        },
      ];

      await dbHelpers.saveMetrics(metrics);
      await dbHelpers.clearMetrics();

      const all = await db.metrics.toArray();
      expect(all).toHaveLength(0);
    });
  });

  describe('Entries', () => {
    it('should save entries to database', async () => {
      const entries: DBEntry[] = [
        {
          id: 1,
          user_id: 1,
          entry_date: '2024-01-15',
          notes: 'Test entry',
          values: [],
        },
      ];

      await dbHelpers.saveEntries(entries);

      const saved = await db.entries.toArray();
      expect(saved).toHaveLength(1);
      expect(saved[0].entry_date).toBe('2024-01-15');
    });

    it('should get all entries', async () => {
      const entries: DBEntry[] = [
        {
          id: 1,
          user_id: 1,
          entry_date: '2024-01-15',
          values: [],
        },
        {
          id: 2,
          user_id: 1,
          entry_date: '2024-01-16',
          values: [],
        },
      ];

      await dbHelpers.saveEntries(entries);

      const all = await dbHelpers.getAllEntries();
      expect(all).toHaveLength(2);
    });

    it('should get entries by date range', async () => {
      const entries: DBEntry[] = [
        {
          id: 1,
          user_id: 1,
          entry_date: '2024-01-10',
          values: [],
        },
        {
          id: 2,
          user_id: 1,
          entry_date: '2024-01-15',
          values: [],
        },
        {
          id: 3,
          user_id: 1,
          entry_date: '2024-01-20',
          values: [],
        },
      ];

      await dbHelpers.saveEntries(entries);

      const rangeEntries = await dbHelpers.getEntriesByDateRange('2024-01-12', '2024-01-18');
      expect(rangeEntries).toHaveLength(1);
      expect(rangeEntries[0].entry_date).toBe('2024-01-15');
    });

    it('should clear all entries', async () => {
      const entries: DBEntry[] = [
        {
          id: 1,
          user_id: 1,
          entry_date: '2024-01-15',
          values: [],
        },
      ];

      await dbHelpers.saveEntries(entries);
      await dbHelpers.clearEntries();

      const all = await db.entries.toArray();
      expect(all).toHaveLength(0);
    });
  });

  describe('Sync Queue', () => {
    it('should add operation to sync queue', async () => {
      await dbHelpers.addToSyncQueue({
        operation: 'create',
        entity: 'metric',
        data: { name_key: 'test' },
        timestamp: Date.now(),
        retry_count: 0,
        status: 'pending',
      });

      const queue = await db.syncQueue.toArray();
      expect(queue).toHaveLength(1);
      expect(queue[0].operation).toBe('create');
    });

    it('should get pending sync operations', async () => {
      await dbHelpers.addToSyncQueue({
        operation: 'create',
        entity: 'metric',
        data: {},
        timestamp: Date.now(),
        retry_count: 0,
        status: 'pending',
      });

      await dbHelpers.addToSyncQueue({
        operation: 'update',
        entity: 'entry',
        data: {},
        timestamp: Date.now(),
        retry_count: 0,
        status: 'completed',
      });

      const pending = await dbHelpers.getPendingSyncOperations();
      expect(pending).toHaveLength(1);
      expect(pending[0].status).toBe('pending');
    });
  });

  describe('User Settings', () => {
    it('should save user setting', async () => {
      await dbHelpers.saveSetting('theme', 'dark');

      const setting = await dbHelpers.getSetting('theme');
      expect(setting).toBe('dark');
    });

    it('should return null for non-existent setting', async () => {
      const setting = await dbHelpers.getSetting('non_existent');
      expect(setting).toBeNull();
    });

    it('should update existing setting', async () => {
      await dbHelpers.saveSetting('theme', 'light');
      await dbHelpers.saveSetting('theme', 'dark');

      const setting = await dbHelpers.getSetting('theme');
      expect(setting).toBe('dark');
    });
  });
});
