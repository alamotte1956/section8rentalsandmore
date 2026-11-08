// concurrency_engine.js - Optimistic UI State Engine & Adaptive Edge Poller
const CONCURRENCY_SYNC = {
  pollingIntervalMs: 8000,
  timer: null,

  async pollEdgeState() {
    if (!window.AUTH_SYSTEM || !window.AUTH_SYSTEM.activeSession) return;
    const session = window.AUTH_SYSTEM.activeSession;

    try {
      const response = await fetch(`/api/sync?userId=${encodeURIComponent(session.userId)}&role=${encodeURIComponent(session.role)}`, {
        cache: 'no-store'
      });

      if (response.ok) {
        const data = await response.json();
        if (data.status === 'SUCCESS' && Array.isArray(data.properties) && data.properties.length > 0) {
          window.state = window.state || {};
          window.state.properties = data.properties;
          if (typeof window.renderPortfolioGrid === 'function') {
            window.renderPortfolioGrid();
          }
        }
      }
    } catch (err) {
      // Local fallback active
    }
  },

  start() {
    if (this.timer) clearInterval(this.timer);
    this.timer = setInterval(() => this.pollEdgeState(), this.pollingIntervalMs);
  },

  stop() {
    if (this.timer) clearInterval(this.timer);
  }
};

window.CONCURRENCY_SYNC = CONCURRENCY_SYNC;

document.addEventListener('DOMContentLoaded', () => CONCURRENCY_SYNC.start());
