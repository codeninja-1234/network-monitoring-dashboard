const cpuValues = [];
const labels = [];

const cpuChart = new Chart(document.getElementById("cpuChart"), {
  type: "line",
  data: {
    labels,
    datasets: [{
      label: "CPU Usage (%)",
      data: cpuValues,
      borderWidth: 2,
      tension: 0.3,
      fill: false
    }]
  },
  options: {
    responsive: true,
    animation: false,
    scales: { y: { min: 0, max: 100 } }
  }
});
