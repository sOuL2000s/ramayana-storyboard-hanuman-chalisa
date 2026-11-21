document.addEventListener('DOMContentLoaded', () => {
    const frames = document.querySelectorAll('.story-frame');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const frameCounter = document.getElementById('frame-counter');
    const storyboardContainer = document.getElementById('storyboard-container');
    const zoomInBtn = document.getElementById('zoomInBtn');
    const zoomOutBtn = document.getElementById('zoomOutBtn');
    const zoomResetBtn = document.getElementById('zoomResetBtn');
    let currentFrameIndex = 0;
    let currentZoom = 1.0; // Initial zoom level
    const zoomStep = 0.1; // How much to zoom in/out each click
    const minZoom = 0.5; // Minimum zoom level
    const maxZoom = 2.0; // Maximum zoom level
    const defaultZoom = 1.0;

    // Function to apply the current zoom level
    function applyZoom() {
        storyboardContainer.style.transform = `scale(${currentZoom})`;
        storyboardContainer.style.transformOrigin = 'top center'; // Zoom from the top center
        
        // Update reset button state
        if (Math.abs(currentZoom - defaultZoom) < 0.01) {
            zoomResetBtn.classList.add('at-reset');
        } else {
            zoomResetBtn.classList.remove('at-reset');
        }
    }

    // Function to adjust the height of the storyboard container dynamically
    function adjustContainerHeight() {
        const activeFrame = frames[currentFrameIndex];
        if (activeFrame) {
            // Get the natural scroll height of the active frame's content
            // We need to temporarily make it visible and remove absolute positioning to get accurate height
            activeFrame.style.position = 'relative';
            activeFrame.style.visibility = 'hidden';
            activeFrame.style.opacity = '0';
            activeFrame.style.transform = 'none';
            activeFrame.style.height = 'auto'; // Allow it to grow naturally

            const contentHeight = activeFrame.scrollHeight; // Get the full height of the content

            // Reset styles
            activeFrame.style.position = '';
            activeFrame.style.visibility = '';
            activeFrame.style.opacity = '';
            activeFrame.style.transform = '';
            activeFrame.style.height = ''; // Revert to CSS defined height (100%)

            // Set the container's height to match the content, with a minimum
            const minHeight = 400; // A reasonable minimum height for the container
            storyboardContainer.style.height = `${Math.max(contentHeight + 80, minHeight)}px`; // Add some buffer for padding
        }
    }

    function updateFrameCounter() {
        frameCounter.textContent = `${currentFrameIndex + 1} / ${frames.length}`;
    }

    function showFrame(index, direction = 'next') {
        // Remove active and exit classes from all frames
        frames.forEach(frame => {
            frame.classList.remove('active', 'exit-left', 'exit-right');
        });

        // If moving from a previous frame, apply exit animation to the old frame
        if (currentFrameIndex !== index) {
            const oldFrame = frames[currentFrameIndex];
            if (oldFrame) {
                if (direction === 'next') {
                    oldFrame.classList.add('exit-left');
                } else {
                    oldFrame.classList.add('exit-right');
                }
            }
        }

        // Set the new current frame
        currentFrameIndex = index;
        const activeFrame = frames[currentFrameIndex];
        if (activeFrame) {
            // Apply entry animation for the new frame
            activeFrame.style.transform = direction === 'next' ? 'translateZ(-100px) translateX(100%) scale(0.8)' : 'translateZ(-100px) translateX(-100%) scale(0.8)';
            void activeFrame.offsetWidth; // Force reflow
            activeFrame.classList.add('active');
            activeFrame.style.transform = ''; // Clear inline transform to allow CSS transition to take over
        }

        updateNavigationButtons();
        updateFrameCounter();
        adjustContainerHeight(); // Adjust height after showing new frame
    }

    function updateNavigationButtons() {
        prevBtn.disabled = currentFrameIndex === 0;
        nextBtn.disabled = currentFrameIndex === frames.length - 1;
    }

    prevBtn.addEventListener('click', () => {
        if (currentFrameIndex > 0) {
            showFrame(currentFrameIndex - 1, 'prev');
        }
    });

    nextBtn.addEventListener('click', () => {
        if (currentFrameIndex < frames.length - 1) {
            showFrame(currentFrameIndex + 1, 'next');
        }
    });

    zoomInBtn.addEventListener('click', () => {
        currentZoom = Math.min(currentZoom + zoomStep, maxZoom);
        applyZoom();
    });

    zoomOutBtn.addEventListener('click', () => {
        currentZoom = Math.max(currentZoom - zoomStep, minZoom);
        applyZoom();
    });

    zoomResetBtn.addEventListener('click', () => {
        currentZoom = defaultZoom;
        applyZoom();
    });

    // Adjust height on window resize and image load
    window.addEventListener('resize', adjustContainerHeight);
    
    // Also adjust height when images load
    frames.forEach(frame => {
        const img = frame.querySelector('img');
        if (img) {
            img.addEventListener('load', adjustContainerHeight);
        }
    });

    // Initialize the first frame and adjust height
    showFrame(0);
    applyZoom(); // Apply initial zoom level
});