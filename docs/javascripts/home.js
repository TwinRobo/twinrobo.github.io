/* Home page: the compare slider, and the hero video for visitors who prefer less motion. */
(function () {
  function init() {
    document.querySelectorAll(".tr-compare").forEach(function (box) {
      var range = box.querySelector(".tr-compare__range");
      if (!range || range.dataset.ready) return;
      range.dataset.ready = "1";
      var set = function () { box.style.setProperty("--pos", range.value + "%"); };
      range.addEventListener("input", set);
      set();
    });
    if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      document.querySelectorAll(".tr-hero-video video").forEach(function (v) {
        v.removeAttribute("autoplay");
        v.pause();
        v.controls = true;
      });
    }
  }
  if (window.document$) window.document$.subscribe(init); // Material's instant navigation
  else document.addEventListener("DOMContentLoaded", init);
})();
