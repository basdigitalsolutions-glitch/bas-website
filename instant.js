// "See it on your own business": asks the assistant server for a preview built from the visitor's website.
// The section stays hidden unless the server reports that the instant preview is switched on.
(function () {
  var API = "https://salon-assistant-gje5.onrender.com";
  var sec = document.getElementById("try-it");
  if (!sec) return;
  var fr = (document.documentElement.lang || "").indexOf("fr") === 0;
  var T = fr ? {
    busy: "Création de votre aperçu… cela peut prendre jusqu’à une minute.",
    ready: "Votre aperçu est prêt : ",
    open: "Ouvrir mon aperçu",
    errors: {
      invalid_url: "Cette adresse ne semble pas valide. Essayez par exemple monsalon.ca.",
      blocked_url: "Cette adresse ne peut pas être utilisée. Entrez l’adresse publique de votre site.",
      fetch_failed: "Nous n’avons pas pu lire ce site. Vérifiez l’adresse, ou demandez une démo personnalisée plus bas.",
      not_enough_info: "Nous n’avons pas trouvé assez d’information sur ce site (services, prix ou heures). Demandez une démo personnalisée plus bas.",
      rate_limited: "Trop d’essais pour le moment. Réessayez plus tard ou demandez une démo plus bas.",
      daily_cap: "Les aperçus instantanés sont complets pour aujourd’hui. Demandez une démo personnalisée plus bas.",
      busy: "Beaucoup d’aperçus en cours. Réessayez dans quelques minutes.",
      build_failed: "Le service n’a pas pu créer l’aperçu. Demandez une démo personnalisée plus bas.",
      other: "Quelque chose n’a pas fonctionné. Demandez une démo personnalisée plus bas."
    }
  } : {
    busy: "Building your preview… this can take up to a minute.",
    ready: "Your preview is ready: ",
    open: "Open my preview",
    errors: {
      invalid_url: "That address does not look valid. Try something like mysalon.ca.",
      blocked_url: "That address cannot be used. Enter your business's public website address.",
      fetch_failed: "We could not read that site. Check the address, or request a personalized demo below.",
      not_enough_info: "We did not find enough on that site (services, prices or hours). Request a personalized demo below.",
      rate_limited: "Too many tries for now. Try again later or request a demo below.",
      daily_cap: "Instant previews are full for today. Request a personalized demo below.",
      busy: "Many previews are running. Try again in a few minutes.",
      build_failed: "The service could not build the preview. Request a personalized demo below.",
      other: "Something went wrong. Request a personalized demo below."
    }
  };

  // Show the section only if the server says the feature is on.
  var ctl = new AbortController();
  var t0 = setTimeout(function () { ctl.abort(); }, 8000);
  fetch(API + "/health", { signal: ctl.signal }).then(function (r) { return r.json(); })
    .then(function (h) { if (h && h.instant === true) sec.hidden = false; })
    .catch(function () {}).then(function () { clearTimeout(t0); });

  var form = document.getElementById("try-form"), input = document.getElementById("try-url"),
      btn = document.getElementById("try-btn"), out = document.getElementById("try-out");

  form.addEventListener("submit", function (ev) {
    ev.preventDefault();
    var url = input.value.trim();
    if (!url) { input.focus(); return; }
    out.textContent = T.busy; btn.disabled = true;
    var c = new AbortController(), timer = setTimeout(function () { c.abort(); }, 90000);
    fetch(API + "/api/instant", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ url: url }), signal: c.signal })
      .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
      .then(function (x) {
        if (!x.ok || !x.j.demo_url) { out.textContent = T.errors[x.j && x.j.error] || T.errors.other; return; }
        var a = document.createElement("a");
        a.className = "btn btn-p"; a.href = x.j.demo_url + (fr ? "" : ""); a.target = "_blank"; a.rel = "noopener"; a.textContent = T.open;
        out.textContent = T.ready + (x.j.name || "") + " "; out.appendChild(a);
      })
      .catch(function () { out.textContent = T.errors.other; })
      .then(function () { clearTimeout(timer); btn.disabled = false; });
  });
})();
