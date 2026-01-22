// DOM Elements
document.addEventListener('DOMContentLoaded', function() {

    // Mobile Menu Toggle
    const mobileToggle = document.querySelector('.mobile-toggle');
    const navMenu = document.querySelector('.nav-menu');

    if (mobileToggle) {
        mobileToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            this.classList.toggle('active');
        });
    }

    // Smooth Scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Product Media Gallery
    const thumbnails = document.querySelectorAll('.thumbnail');
    const mainMedia = document.querySelector('.media-main');

    thumbnails.forEach(thumbnail => {
        thumbnail.addEventListener('click', function() {
            const mediaContent = this.innerHTML;
            mainMedia.innerHTML = mediaContent;

            // Remove active class from all thumbnails
            thumbnails.forEach(t => t.classList.remove('active'));
            // Add active class to clicked thumbnail
            this.classList.add('active');
        });
    });

    // Form Validation
    const orderForm = document.querySelector('.order-form');
    if (orderForm) {
        orderForm.addEventListener('submit', function(e) {
            const phoneInput = document.getElementById('phone_number');
            const phoneValue = phoneInput.value.trim();

            // Simple phone validation
            const phoneRegex = /^[\d\s+()-]+$/;
            if (!phoneRegex.test(phoneValue)) {
                e.preventDefault();
                alert('Խնդրում ենք մուտքագրել ճիշտ հեռախոսահամար');
                phoneInput.focus();
                return false;
            }
        });
    }

    // Auto-hide success messages
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });

    // Scroll to top button
    const scrollBtn = createScrollToTopButton();

    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            scrollBtn.classList.add('visible');
        } else {
            scrollBtn.classList.remove('visible');
        }
    });

    // Lazy loading for images
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                observer.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));

    // Animation on scroll
    const animateOnScroll = () => {
        const elements = document.querySelectorAll('.feature-card, .template-card');

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, {
            threshold: 0.1
        });

        elements.forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            observer.observe(el);
        });
    };

    animateOnScroll();
});

// Helper function to create scroll-to-top button
function createScrollToTopButton() {
    const btn = document.createElement('button');
    btn.innerHTML = '↑';
    btn.className = 'scroll-to-top';
    btn.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background-color: #000;
        color: #fff;
        border: none;
        font-size: 1.5rem;
        cursor: pointer;
        opacity: 0;
        visibility: hidden;
        transition: all 0.3s ease;
        z-index: 999;
    `;

    btn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    document.body.appendChild(btn);

    // Add visible class styles
    const style = document.createElement('style');
    style.textContent = `
        .scroll-to-top.visible {
            opacity: 1;
            visibility: visible;
        }
        .scroll-to-top:hover {
            background-color: #333;
            transform: translateY(-5px);
        }
    `;
    document.head.appendChild(style);

    return btn;
}

// Page loader
window.addEventListener('load', function() {
    document.body.classList.add('loaded');
});