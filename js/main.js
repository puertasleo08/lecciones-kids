(function () {
  const modal = document.getElementById("premium-modal");
  const minutesEl = document.querySelector("[data-minutes]");
  const secondsEl = document.querySelector("[data-seconds]");
  const INTERVAL = 900;
  const STORAGE_KEY = "lk-math-countdown";

  function openModal() {
    if (!modal) return;
    modal.classList.add("is-open");
    modal.setAttribute("aria-hidden", "false");
    document.body.classList.add("modal-open");
    const closeBtn = modal.querySelector(".modal-close");
    if (closeBtn) closeBtn.focus();
  }

  function closeModal() {
    if (!modal) return;
    modal.classList.remove("is-open");
    modal.setAttribute("aria-hidden", "true");
    document.body.classList.remove("modal-open");
  }

  document.querySelectorAll('a[href="#AbrirPremium"]').forEach((link) => {
    link.addEventListener("click", (event) => {
      event.preventDefault();
      openModal();
    });
  });

  if (modal) {
    modal.querySelector(".modal-backdrop")?.addEventListener("click", closeModal);
    modal.querySelector(".modal-close")?.addEventListener("click", closeModal);
  }

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") closeModal();
  });

  if (window.location.hash === "#AbrirPremium") {
    openModal();
  }

  let exitShown = sessionStorage.getItem("lk-exit-shown") === "1";
  document.documentElement.addEventListener("mouseleave", (event) => {
    if (exitShown || event.clientY > 0) return;
    exitShown = true;
    sessionStorage.setItem("lk-exit-shown", "1");
    openModal();
  });

  function remaining() {
    const saved = Number(sessionStorage.getItem(STORAGE_KEY) || 0);
    const now = Date.now();
    if (!saved || saved <= now) {
      const end = now + INTERVAL * 1000;
      sessionStorage.setItem(STORAGE_KEY, String(end));
      return INTERVAL;
    }
    return Math.max(0, Math.floor((saved - now) / 1000));
  }

  function renderCountdown(total) {
    if (!minutesEl || !secondsEl) return;
    const mins = Math.floor(total / 60);
    const secs = total % 60;
    minutesEl.textContent = String(mins).padStart(2, "0");
    secondsEl.textContent = String(secs).padStart(2, "0");
  }

  let left = remaining();
  renderCountdown(left);
  const timer = setInterval(() => {
    left -= 1;
    if (left <= 0) {
      left = 0;
      clearInterval(timer);
      document.querySelector(".countdown")?.setAttribute("hidden", "");
    }
    renderCountdown(left);
  }, 1000);

  document.querySelectorAll(".faq-item").forEach((item) => {
    const button = item.querySelector("button");
    button?.addEventListener("click", () => {
      const open = item.classList.contains("is-open");
      document.querySelectorAll(".faq-item").forEach((other) => {
        other.classList.remove("is-open");
        other.querySelector("button")?.setAttribute("aria-expanded", "false");
      });
      if (!open) {
        item.classList.add("is-open");
        button.setAttribute("aria-expanded", "true");
      }
    });
  });

  const viewport = document.querySelector(".slider-viewport");
  if (viewport) {
    const prev = document.querySelector(".slider-prev");
    const next = document.querySelector(".slider-next");
    const scrollBySlide = (direction) => {
      const max = viewport.scrollWidth - viewport.clientWidth;
      if (direction > 0 && viewport.scrollLeft >= max - 8) {
        viewport.scrollTo({ left: 0, behavior: "smooth" });
        return;
      }
      if (direction < 0 && viewport.scrollLeft <= 8) {
        viewport.scrollTo({ left: max, behavior: "smooth" });
        return;
      }
      viewport.scrollBy({ left: direction * viewport.clientWidth, behavior: "smooth" });
    };
    prev?.addEventListener("click", () => scrollBySlide(-1));
    next?.addEventListener("click", () => scrollBySlide(1));
    viewport.addEventListener("keydown", (event) => {
      if (event.key === "ArrowLeft") {
        event.preventDefault();
        scrollBySlide(-1);
      }
      if (event.key === "ArrowRight") {
        event.preventDefault();
        scrollBySlide(1);
      }
    });
  }
})();
