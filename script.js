/**
 * Cachly Website - JavaScript
 * Handles navigation, animations, and interactive elements
 */

document.addEventListener('DOMContentLoaded', function() {
    // ===== Elements =====
    const navbar = document.getElementById('navbar');
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');
    const navLinks = navMenu.querySelectorAll('a');
    const heroParallax = document.querySelector('.hero-parallax');
    const carplayParallax = document.querySelector('.carplay-parallax');
    const downloadParallax = document.querySelector('.download-parallax');
    const featureCards = document.querySelectorAll('.feature-card');

    // ===== Navbar Scroll Effect =====
    let lastScroll = 0;
    const scrollThreshold = 50;

    function handleNavbarScroll() {
        const currentScroll = window.pageYOffset;

        if (currentScroll > scrollThreshold) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }

        lastScroll = currentScroll;
    }

    // ===== Mobile Menu Toggle =====
    function toggleMobileMenu() {
        navToggle.classList.toggle('active');
        navMenu.classList.toggle('active');
        document.body.style.overflow = navMenu.classList.contains('active') ? 'hidden' : '';
    }

    function closeMobileMenu() {
        navToggle.classList.remove('active');
        navMenu.classList.remove('active');
        document.body.style.overflow = '';
        // Close dropdown when menu closes
        const navDropdown = document.querySelector('.nav-dropdown');
        if (navDropdown) {
            navDropdown.classList.remove('active');
        }
    }

    navToggle.addEventListener('click', toggleMobileMenu);

    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (window.innerWidth <= 768) {
                // Don't close menu when clicking the dropdown toggle
                if (!this.classList.contains('dropdown-toggle')) {
                    closeMobileMenu();
                }
            }
        });
    });

    // ===== Mobile Dropdown Toggle =====
    const dropdownToggle = document.querySelector('.dropdown-toggle');
    const navDropdown = document.querySelector('.nav-dropdown');

    if (dropdownToggle && navDropdown) {
        dropdownToggle.addEventListener('click', function(e) {
            if (window.innerWidth <= 768) {
                e.preventDefault();
                navDropdown.classList.toggle('active');
            }
        });

        // Prevent dropdown links from closing the mobile menu immediately
        const dropdownLinks = navDropdown.querySelectorAll('.dropdown-menu a');
        dropdownLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                e.stopPropagation();
                if (window.innerWidth <= 768) {
                    setTimeout(closeMobileMenu, 150);
                }
            });
        });
    }

    // Close menu on resize to desktop
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768) {
            closeMobileMenu();
        }
    });

    // ===== Smooth Scroll for Anchor Links =====
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');

            if (href === '#') return;

            e.preventDefault();

            const target = document.querySelector(href);
            if (target) {
                const navbarHeight = navbar.offsetHeight;
                const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - navbarHeight;

                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

    // ===== Parallax Effect =====
    function handleParallax() {
        const scrolled = window.pageYOffset;
        const rate = 0.3;

        if (heroParallax) {
            heroParallax.style.transform = `translateY(${scrolled * rate}px)`;
        }

        if (carplayParallax) {
            const carplaySection = carplayParallax.parentElement;
            const carplayOffset = carplaySection.offsetTop;
            const carplayScroll = scrolled - carplayOffset;

            if (carplayScroll > -window.innerHeight && carplayScroll < carplaySection.offsetHeight) {
                carplayParallax.style.transform = `translateY(${carplayScroll * rate * 0.5}px)`;
            }
        }

        if (downloadParallax) {
            const downloadSection = downloadParallax.parentElement;
            const downloadOffset = downloadSection.offsetTop;
            const downloadScroll = scrolled - downloadOffset;

            if (downloadScroll > -window.innerHeight && downloadScroll < downloadSection.offsetHeight) {
                downloadParallax.style.transform = `translateY(${downloadScroll * rate * 0.5}px)`;
            }
        }
    }

    // ===== Intersection Observer for Animations =====
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const animationObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animationPlayState = 'running';
                animationObserver.unobserve(entry.target);
            }
        });
    }, observerOptions);

    featureCards.forEach(card => {
        card.style.animationPlayState = 'paused';
        animationObserver.observe(card);
    });

    // ===== Scroll Event Handler =====
    let ticking = false;

    function onScroll() {
        if (!ticking) {
            window.requestAnimationFrame(() => {
                handleNavbarScroll();
                handleParallax();
                ticking = false;
            });
            ticking = true;
        }
    }

    window.addEventListener('scroll', onScroll, { passive: true });

    // ===== Hero Screenshot 3D Effect =====
    const heroScreenshot = document.querySelector('.hero-screenshot');

    if (heroScreenshot) {
        heroScreenshot.addEventListener('mousemove', function(e) {
            if (window.innerWidth <= 1024) return;

            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateX = (y - centerY) / 20;
            const rotateY = (centerX - x) / 20;

            this.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
        });

        heroScreenshot.addEventListener('mouseleave', function() {
            this.style.transform = 'perspective(1000px) rotateY(-5deg) rotateX(5deg)';
        });
    }

    // ===== CarPlay Images Hover Effect =====
    const carplayScreens = document.querySelectorAll('.carplay-screen');

    carplayScreens.forEach(screen => {
        screen.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.03) translateZ(20px)';
            this.style.zIndex = '10';
        });

        screen.addEventListener('mouseleave', function() {
            if (this.classList.contains('carplay-screen-1')) {
                this.style.transform = 'translateX(20px)';
            } else {
                this.style.transform = 'translateX(-20px)';
            }
            this.style.zIndex = '1';
        });
    });

    // ===== Screenshot Carousel =====
    const carouselContainer = document.getElementById('screenshotCarousel');
    const carousel = carouselContainer ? carouselContainer.querySelector('.carousel') : null;
    const carouselTrack = carouselContainer ? carouselContainer.querySelector('.carousel-track') : null;
    const slides = carouselContainer ? carouselContainer.querySelectorAll('.carousel-slide') : [];
    const prevBtn = document.getElementById('carouselPrev');
    const nextBtn = document.getElementById('carouselNext');
    const indicators = document.querySelectorAll('.indicator');
    const progressBar = document.getElementById('carouselProgress');

    let currentSlide = 0;
    let autoSlideInterval = null;
    let progressInterval = null;
    const autoSlideDelay = 5000; // 5 seconds per slide
    const progressUpdateInterval = 50; // Update progress every 50ms

    function updateCarousel(direction = 'next') {
        if (!carouselTrack || slides.length === 0) return;

        // Remove active and animation classes from all slides
        slides.forEach(slide => {
            slide.classList.remove('active', 'slide-in-right', 'slide-in-left');
        });

        // Update indicators
        indicators.forEach((indicator, index) => {
            indicator.classList.toggle('active', index === currentSlide);
        });

        // Add animation class based on direction
        const animationClass = direction === 'next' ? 'slide-in-right' : 'slide-in-left';
        slides[currentSlide].classList.add('active', animationClass);

        // Move the track
        carouselTrack.style.transform = `translateX(-${currentSlide * 100}%)`;

        // Reset progress bar
        resetProgress();
    }

    function nextSlide() {
        currentSlide = (currentSlide + 1) % slides.length;
        updateCarousel('next');
    }

    function prevSlide() {
        currentSlide = (currentSlide - 1 + slides.length) % slides.length;
        updateCarousel('prev');
    }

    function goToSlide(index) {
        const direction = index > currentSlide ? 'next' : 'prev';
        currentSlide = index;
        updateCarousel(direction);
    }

    function resetProgress() {
        if (!progressBar) return;

        // Clear existing progress interval
        if (progressInterval) {
            clearInterval(progressInterval);
        }

        // Reset progress bar
        progressBar.style.width = '0%';

        // Start new progress animation
        let progress = 0;
        const increment = (progressUpdateInterval / autoSlideDelay) * 100;

        progressInterval = setInterval(() => {
            progress += increment;
            progressBar.style.width = `${Math.min(progress, 100)}%`;

            if (progress >= 100) {
                clearInterval(progressInterval);
            }
        }, progressUpdateInterval);
    }

    function startAutoSlide() {
        if (autoSlideInterval) {
            clearInterval(autoSlideInterval);
        }

        resetProgress();

        autoSlideInterval = setInterval(() => {
            nextSlide();
        }, autoSlideDelay);
    }

    function stopAutoSlide() {
        if (autoSlideInterval) {
            clearInterval(autoSlideInterval);
            autoSlideInterval = null;
        }
        if (progressInterval) {
            clearInterval(progressInterval);
            progressInterval = null;
        }
    }

    function restartAutoSlide() {
        stopAutoSlide();
        startAutoSlide();
    }

    // Event listeners for carousel controls
    if (prevBtn) {
        prevBtn.addEventListener('click', () => {
            prevSlide();
            restartAutoSlide();
        });
    }

    if (nextBtn) {
        nextBtn.addEventListener('click', () => {
            nextSlide();
            restartAutoSlide();
        });
    }

    // Indicator click events
    indicators.forEach((indicator, index) => {
        indicator.addEventListener('click', () => {
            goToSlide(index);
            restartAutoSlide();
        });
    });

    // Pause auto-slide on hover
    if (carouselContainer) {
        carouselContainer.addEventListener('mouseenter', stopAutoSlide);
        carouselContainer.addEventListener('mouseleave', startAutoSlide);

        // Touch/swipe support for carousel
        let carouselTouchStartX = 0;
        let carouselTouchEndX = 0;

        carouselContainer.addEventListener('touchstart', (e) => {
            carouselTouchStartX = e.changedTouches[0].screenX;
            stopAutoSlide();
        }, { passive: true });

        carouselContainer.addEventListener('touchend', (e) => {
            carouselTouchEndX = e.changedTouches[0].screenX;
            const diff = carouselTouchStartX - carouselTouchEndX;
            const swipeThreshold = 50;

            if (Math.abs(diff) > swipeThreshold) {
                if (diff > 0) {
                    nextSlide();
                } else {
                    prevSlide();
                }
            }
            restartAutoSlide();
        }, { passive: true });
    }

    // Keyboard navigation for carousel
    document.addEventListener('keydown', (e) => {
        if (!carouselContainer) return;

        const carouselRect = carouselContainer.getBoundingClientRect();
        const isInViewport = carouselRect.top < window.innerHeight && carouselRect.bottom > 0;

        if (isInViewport) {
            if (e.key === 'ArrowLeft') {
                prevSlide();
                restartAutoSlide();
            } else if (e.key === 'ArrowRight') {
                nextSlide();
                restartAutoSlide();
            }
        }
    });

    // Start carousel when in viewport
    const carouselObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                startAutoSlide();
            } else {
                stopAutoSlide();
            }
        });
    }, { threshold: 0.3 });

    if (carouselContainer) {
        carouselObserver.observe(carouselContainer);
    }


    // ===== Lazy Loading Images =====
    const lazyImages = document.querySelectorAll('img[data-src]');

    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                imageObserver.unobserve(img);
            }
        });
    }, { rootMargin: '50px' });

    lazyImages.forEach(img => imageObserver.observe(img));

    // ===== Keyboard Navigation =====
    document.addEventListener('keydown', function(e) {
        // Close mobile menu on Escape
        if (e.key === 'Escape' && navMenu.classList.contains('active')) {
            closeMobileMenu();
        }
    });

    // ===== Touch Events for Mobile =====
    let touchStartX = 0;
    let touchEndX = 0;

    document.addEventListener('touchstart', function(e) {
        touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });

    document.addEventListener('touchend', function(e) {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    }, { passive: true });

    function handleSwipe() {
        const swipeThreshold = 100;
        const diff = touchStartX - touchEndX;

        // Swipe left to close menu
        if (diff > swipeThreshold && navMenu.classList.contains('active')) {
            closeMobileMenu();
        }
    }

    // ===== Performance: Reduce animations for users who prefer reduced motion =====
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

    if (prefersReducedMotion.matches) {
        // Disable parallax
        window.removeEventListener('scroll', handleParallax);

        // Remove animation delays
        featureCards.forEach(card => {
            card.style.animationDelay = '0s';
        });
    }

    // ===== Set Current Year =====
    const currentYearEl = document.getElementById('currentYear');
    if (currentYearEl) {
        currentYearEl.textContent = new Date().getFullYear();
    }

    // ===== Initialize =====
    handleNavbarScroll();

    // Trigger animations for elements in viewport on load
    setTimeout(() => {
        featureCards.forEach(card => {
            const rect = card.getBoundingClientRect();
            if (rect.top < window.innerHeight) {
                card.style.animationPlayState = 'running';
            }
        });
    }, 100);

    // ===== Features Modal =====
    const showAllFeaturesBtn = document.getElementById('showAllFeatures');
    const featuresModal = document.getElementById('featuresModal');
    const closeModalBtn = document.getElementById('closeModal');

    if (showAllFeaturesBtn && featuresModal) {
        showAllFeaturesBtn.addEventListener('click', function(e) {
            e.preventDefault();
            featuresModal.classList.add('active');
            document.body.style.overflow = 'hidden';
        });
    }

    if (closeModalBtn && featuresModal) {
        closeModalBtn.addEventListener('click', function() {
            featuresModal.classList.remove('active');
            document.body.style.overflow = '';
        });
    }

    if (featuresModal) {
        featuresModal.addEventListener('click', function(e) {
            if (e.target === featuresModal) {
                featuresModal.classList.remove('active');
                document.body.style.overflow = '';
            }
        });

        // Close modal on Escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && featuresModal.classList.contains('active')) {
                featuresModal.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    }

    console.log('Cachly website initialized');
});

// ===== Service Worker Registration (for PWA support) =====
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        // Service worker can be added for offline support
        // navigator.serviceWorker.register('/sw.js');
    });
}
