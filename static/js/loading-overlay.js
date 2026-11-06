
/**
 * Loading Spinner Overlay
 */
class LoadingOverlay {
    constructor(container_id) {
        this.container = container_id ? document.getElementById(container_id) : document.body;
        this.element = document.createElement('div');
        this.element.classList.add('loading-overlay');
        this.element.innerHTML = `<div class="spinner"></div>`;
        this.container.append(this.element);
    }

    show() {
        this.element.classList.add('active');
        document.body.style.overflow = 'hidden'; // Optional: Locks scrolling while active
    }
  
    hide() {
        this.element.classList.remove('active');
        document.body.style.overflow = ''; // Restores window scrolling
    }
}
