import { writable } from 'svelte/store';
import { dbHelpers, SyncOperation } from './db';
import api from './api';

// Sync status interface
export interface SyncStatus {
  isOnline: boolean;
  isSyncing: boolean;
  pendingCount: number;
  lastSyncTime: number | null;
  error: string | null;
}

// Create sync status store
const initialStatus: SyncStatus = {
  isOnline: navigator.onLine,
  isSyncing: false,
  pendingCount: 0,
  lastSyncTime: null,
  error: null
};

export const syncStatus = writable<SyncStatus>(initialStatus);

// Sync manager class
class SyncManager {
  private syncInterval: number | null = null;
  private processingQueue = false;

  constructor() {
    // Listen to online/offline events
    window.addEventListener('online', () => this.handleOnline());
    window.addEventListener('offline', () => this.handleOffline());

    // Initialize sync status
    this.updatePendingCount();

    // Start auto-sync interval (every 30 seconds when online)
    this.startAutoSync();
  }

  private handleOnline() {
    syncStatus.update(s => ({ ...s, isOnline: true }));
    this.processQueue();
  }

  private handleOffline() {
    syncStatus.update(s => ({ ...s, isOnline: false, isSyncing: false }));
  }

  private startAutoSync() {
    this.syncInterval = window.setInterval(() => {
      if (navigator.onLine && !this.processingQueue) {
        this.processQueue();
      }
    }, 30000); // 30 seconds
  }

  stopAutoSync() {
    if (this.syncInterval) {
      clearInterval(this.syncInterval);
      this.syncInterval = null;
    }
  }

  async addToQueue(
    operation: 'CREATE' | 'UPDATE' | 'DELETE',
    entity: 'metric' | 'entry' | 'user',
    data: any,
    entity_id?: number
  ): Promise<void> {
    const syncOp: Omit<SyncOperation, 'id'> = {
      operation,
      entity,
      entity_id,
      data,
      timestamp: Date.now(),
      retry_count: 0,
      status: 'pending'
    };

    await dbHelpers.addToSyncQueue(syncOp);
    await this.updatePendingCount();

    // Try to sync immediately if online
    if (navigator.onLine) {
      setTimeout(() => this.processQueue(), 100);
    }
  }

  async processQueue(): Promise<void> {
    if (this.processingQueue || !navigator.onLine) {
      return;
    }

    this.processingQueue = true;
    syncStatus.update(s => ({ ...s, isSyncing: true, error: null }));

    try {
      const operations = await dbHelpers.getPendingSyncOperations();

      for (const op of operations) {
        try {
          // Mark as processing
          await dbHelpers.updateSyncOperation(op.id!, { status: 'processing' });

          // Execute the operation
          await this.executeSyncOperation(op);

          // Remove from queue on success
          await dbHelpers.deleteSyncOperation(op.id!);
        } catch (error: any) {
          console.error(`Sync operation ${op.id} failed:`, error);

          // Update retry count
          const retry_count = (op.retry_count || 0) + 1;

          if (retry_count >= 5) {
            // Max retries reached, mark as failed
            await dbHelpers.updateSyncOperation(op.id!, {
              status: 'failed',
              retry_count,
              error: error.message || 'Unknown error'
            });
          } else {
            // Retry later
            await dbHelpers.updateSyncOperation(op.id!, {
              status: 'pending',
              retry_count
            });
          }
        }
      }

      syncStatus.update(s => ({
        ...s,
        lastSyncTime: Date.now(),
        error: null
      }));
    } catch (error: any) {
      console.error('Sync queue processing failed:', error);
      syncStatus.update(s => ({
        ...s,
        error: error.message || 'Sync failed'
      }));
    } finally {
      this.processingQueue = false;
      syncStatus.update(s => ({ ...s, isSyncing: false }));
      await this.updatePendingCount();
    }
  }

  private async executeSyncOperation(op: SyncOperation): Promise<void> {
    const { operation, entity, entity_id, data } = op;

    switch (entity) {
      case 'metric':
        if (operation === 'CREATE') {
          await api.post('/metrics', data);
        } else if (operation === 'UPDATE' && entity_id) {
          await api.patch(`/metrics/${entity_id}`, data);
        } else if (operation === 'DELETE' && entity_id) {
          await api.delete(`/metrics/${entity_id}`);
        }
        break;

      case 'entry':
        if (operation === 'CREATE') {
          await api.post('/entries', data);
        } else if (operation === 'UPDATE' && entity_id) {
          await api.patch(`/entries/${entity_id}`, data);
        } else if (operation === 'DELETE' && entity_id) {
          await api.delete(`/entries/${entity_id}`);
        }
        break;

      case 'user':
        if (operation === 'UPDATE') {
          await api.patch('/users/me', data);
        } else if (operation === 'DELETE') {
          await api.delete('/users/me');
        }
        break;

      default:
        throw new Error(`Unknown entity type: ${entity}`);
    }
  }

  async updatePendingCount(): Promise<void> {
    const operations = await dbHelpers.getPendingSyncOperations();
    syncStatus.update(s => ({ ...s, pendingCount: operations.length }));
  }

  async clearQueue(): Promise<void> {
    await dbHelpers.clearSyncQueue();
    await this.updatePendingCount();
  }

  async forceSyncNow(): Promise<void> {
    if (navigator.onLine) {
      await this.processQueue();
    }
  }
}

// Create and export singleton instance
export const syncManager = new SyncManager();

// Export convenience functions
export const syncActions = {
  forceSyncNow: () => syncManager.forceSyncNow(),
  clearQueue: () => syncManager.clearQueue(),
  addToQueue: (
    operation: 'CREATE' | 'UPDATE' | 'DELETE',
    entity: 'metric' | 'entry' | 'user',
    data: any,
    entity_id?: number
  ) => syncManager.addToQueue(operation, entity, data, entity_id)
};
