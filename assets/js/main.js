(function () {
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
    sidebar.classList.add("is-open");
    if (backdrop) backdrop.hidden = false;
    if (menuBtn) menuBtn.setAttribute("aria-expanded", "true");
  }
  function closeMenu() {
    sidebar.classList.remove("is-open");
    if (backdrop) backdrop.hidden = true;
    if (menuBtn) menuBtn.setAttribute("aria-expanded", "false");
  }

  menuBtn?.addEventListener("click", () => {
    const isOpen = sidebar.classList.contains("is-open");
    isOpen ? closeMenu() : openMenu();
  });
  backdrop?.addEventListener("click", closeMenu);

  // Smooth scroll + active link
  function setActiveById(id) {
    navLinks.forEach(a => a.classList.toggle("is-active", a.getAttribute("href") === "#" + id));
  }

  navLinks.forEach(a => {
    a.addEventListener("click", (e) => {
      const href = a.getAttribute("href");
      if (!href || !href.startsWith("#")) return;

      e.preventDefault();
      const id = href.slice(1);
      const target = document.getElementById(id);
      if (!target) return;

      // Scroll inside the main scroll container on desktop, normal on mobile
      const isMobile = window.matchMedia("(max-width: 780px)").matches;

      if (!isMobile && mainScroll) {
        const top = target.offsetTop;
        mainScroll.scrollTo({ top, behavior: "smooth" });
      } else {
        target.scrollIntoView({ behavior: "smooth", block: "start" });
      }

      history.replaceState(null, "", href);
      setActiveById(id);
      closeMenu();
    });
  });

  // Highlight active section while scrolling (desktop container or window)
  const observer = new IntersectionObserver((entries) => {
    const visible = entries
      .filter(e => e.isIntersecting)
      .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];

    if (visible?.target?.id) {
      setActiveById(visible.target.id);
    }
  }, { root: mainScroll || null, threshold: [0.35, 0.55, 0.75] });

  sections.forEach(s => observer.observe(s));

  // Initial active based on hash
  const initial = (location.hash || "#welcome").slice(1);
  setActiveById(initial);

  // ---- Demo chatbot UI ----
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

  function demoReply(userText) {
    const t = userText.toLowerCase();

    if (t.includes("library")) {
      return "Library: tell me if you need hours, study rooms, printing, or finding books and I’ll guide you.";
    }
    if (t.includes("tutor") || t.includes("tutoring")) {
      return "Tutoring: tell me your course code (e.g., COMP/STAT/MATH) and I’ll suggest the best support path.";
    }
    if (t.includes("deadline") || t.includes("exam") || t.includes("deferral")) {
      return "Deadlines/exams: share the course code + what deadline (withdrawal, deferral, assignment) and I’ll point you to the right page/office.";
    }
    if (t.includes("it") || t.includes("wifi") || t.includes("password")) {
      return "IT help: I can guide you for Wi-Fi, passwords, Brightspace access, or account issues. What’s the problem?";
    }
    return "I can help. Choose an area: courses, registration, campus services, IT support, or directions.";
  }

  chatForm?.addEventListener("submit", (e) => {
    e.preventDefault();
    const text = (chatText?.value || "").trim();
    if (!text) return;

    addMsg("user", text);
    chatText.value = "";

    try {
    const res = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text })
    });

    const data = await res.json();
    addMsg("bot", data.answer || "No answer returned.");
  } catch (err) {
    addMsg("bot", "Backend not running. Start it on port 8000.");
  }
});
