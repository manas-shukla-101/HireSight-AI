document.addEventListener("DOMContentLoaded", () => {
  const scoreCanvas = document.getElementById("scoreChart");
  if (!scoreCanvas) return;

  const scores = JSON.parse(scoreCanvas.dataset.scores || "[]");
  if (!scores.length) return;

  const labels = scores.map((_, idx) => `Run ${idx + 1}`);

  new Chart(scoreCanvas, {
    type: "line",
    data: {
      labels,
      datasets: [
        {
          label: "Match Score (%)",
          data: scores,
          borderColor: "#39d0a8",
          backgroundColor: "rgba(57, 208, 168, 0.2)",
          tension: 0.3,
          fill: true,
          pointRadius: 4,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          min: 0,
          max: 100,
        },
      },
    },
  });
});
