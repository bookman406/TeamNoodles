const navLinks = Array.from(document.querySelectorAll(".nav-link"));
const sections = Array.from(document.querySelectorAll("section.section"));
const yearEl = document.getElementById("year");
const yearFooterEl = document.getElementById("yearFooter");

const sidebar = document.getElementById("sidebar");
const menuBtn = document.getElementById("menuBtn");
const backdrop = document.getElementById("backdrop");
const mainScroll = document.getElementById("mainScroll");

// Years
const y = new Date().getFullYear();
if (yearEl) yearEl.textContent = y;
if (yearFooterEl) yearFooterEl.textContent = y;

// Mobile menu
function openMenu() {
  if (sidebar) sidebar.classList.add("is-open");
  if (backdrop) backdrop.hidden = false;
  if (menuBtn) menuBtn.setAttribute("aria-expanded", "true");
}

function closeMenu() {
  if (sidebar) sidebar.classList.remove("is-open");
  if (backdrop) backdrop.hidden = true;
  if (menuBtn) menuBtn.setAttribute("aria-expanded", "false");
}

menuBtn?.addEventListener("click", () => {
  const isOpen = sidebar?.classList.contains("is-open");
  isOpen ? closeMenu() : openMenu();
});

backdrop?.addEventListener("click", closeMenu);

// Smooth scroll + active nav
function setActiveById(id) {
  navLinks.forEach(a => {
    a.classList.toggle("is-active", a.getAttribute("href") === "#" + id);
  });
}

navLinks.forEach(a => {
  a.addEventListener("click", e => {
    const href = a.getAttribute("href");
    if (!href || !href.startsWith("#")) return;

    e.preventDefault();
    const id = href.slice(1);
    const target = document.getElementById(id);
    if (!target) return;

    const isMobile = window.matchMedia("(max-width: 780px)").matches;

    if (!isMobile && mainScroll) {
      mainScroll.scrollTo({
        top: target.offsetTop,
        behavior: "smooth"
      });
    } else {
      target.scrollIntoView({
        behavior: "smooth",
        block: "start"
      });
    }

    history.replaceState(null, "", href);
    setActiveById(id);
    closeMenu();
  });
});

// Highlight active section while scrolling
const observer = new IntersectionObserver(
  entries => {
    const visible = entries
      .filter(e => e.isIntersecting)
      .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];

    if (visible?.target?.id) {
      setActiveById(visible.target.id);
    }
  },
  {
    root: mainScroll || null,
    threshold: [0.35, 0.55, 0.75]
  }
);

sections.forEach(section => observer.observe(section));

// Initial active state
const initial = (location.hash || "#welcome").slice(1);
setActiveById(initial);

// Chatbot
const chatForm = document.getElementById("chatForm");
const chatText = document.getElementById("chatText");
const chatMessages = document.getElementById("chatMessages");

function addMsg(role, text) {
  if (!chatMessages) return;

  const wrap = document.createElement("div");
  wrap.className = `msg ${role}`;

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;

  wrap.appendChild(bubble);
  chatMessages.appendChild(wrap);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

chatForm?.addEventListener("submit", async e => {
  e.preventDefault();

  const text = (chatText?.value || "").trim();
  if (!text) return;

  addMsg("user", text);
  chatText.value = "";

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message: text })
    });

    if (!res.ok) {
      throw new Error(`HTTP error ${res.status}`);
    }

    const data = await res.json();
    addMsg("bot", data.answer || "No answer returned.");
  } catch (err) {
    addMsg("bot", "Could not connect to backend.");
    console.error(err);
  }
});

// Contact form demo
const contactForm = document.getElementById("contactForm");
const contactNote = document.getElementById("contactNote");

contactForm?.addEventListener("submit", e => {
  e.preventDefault();
  if (contactNote) {
    contactNote.textContent = "Thanks! This is a demo form (no backend connected yet).";
  }
});

// Hero banner slider
const heroSlides = document.querySelectorAll(".hero-banner-slide");
const heroDots = document.querySelectorAll(".hero-dot");
const heroPrev = document.getElementById("heroPrev");
const heroNext = document.getElementById("heroNext");

let currentSlide = 0;
let heroInterval = null;

function showSlide(index) {
  if (!heroSlides.length) return;

  heroSlides.forEach((slide, i) => {
    slide.classList.toggle("active", i === index);
  });

  heroDots.forEach((dot, i) => {
    dot.classList.toggle("active", i === index);
  });

  currentSlide = index;
}

function nextSlide() {
  if (!heroSlides.length) return;
  showSlide((currentSlide + 1) % heroSlides.length);
}

function prevSlide() {
  if (!heroSlides.length) return;
  showSlide((currentSlide - 1 + heroSlides.length) % heroSlides.length);
}

function startHeroAuto() {
  if (!heroSlides.length) return;
  heroInterval = setInterval(nextSlide, 3500);
}

function restartHeroAuto() {
  if (heroInterval) clearInterval(heroInterval);
  startHeroAuto();
}

heroNext?.addEventListener("click", () => {
  nextSlide();
  restartHeroAuto();
});

heroPrev?.addEventListener("click", () => {
  prevSlide();
  restartHeroAuto();
});

heroDots.forEach(dot => {
  dot.addEventListener("click", () => {
    const index = Number(dot.dataset.slide);
    showSlide(index);
    restartHeroAuto();
  });
});

if (heroSlides.length) {
  showSlide(0);
  startHeroAuto();
}