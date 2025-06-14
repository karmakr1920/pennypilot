(function ($) {
  'use strict';
  $.fn.andSelf = function () {
    return this.addBack.apply(this, arguments);
  }
  $(function () {

    //check all boxes in order status 
    $("#check-all").click(function () {
      $(".form-check-input").prop('checked', $(this).prop('checked'));
    });

    if (document.getElementById("transaction-history")) {
      const doughnutChartCanvas = document.getElementById('transaction-history');
      const hasData = window.hasCategoryData;
      const labels = window.categoryLabels || [];
      const data = window.categoryData || [];
      const colors = window.categoryColors || [];

      // Custom tooltip handler to render outside the chart
      const externalTooltipHandler = (context) => {
        const { chart, tooltip } = context;
        const tooltipEl = document.getElementById('chart-tooltip');

        // Hide if no tooltip
        if (tooltip.opacity === 0) {
          tooltipEl.style.display = 'none';
          return;
        }

        // Set tooltip content
        if (tooltip.body) {
          const titleLines = tooltip.title || [];
          const bodyLines = tooltip.body.map(b => b.lines);
          let innerHtml = '';

          titleLines.forEach(title => {
            innerHtml += `<div>${title}: ₹${tooltip.dataPoints[0].raw.toFixed(2)}</div>`;
          });

          tooltipEl.innerHTML = innerHtml;
        }

        // Position tooltip outside the chart
        const { offsetLeft: positionX, offsetTop: positionY } = chart.canvas;
        tooltipEl.style.display = 'block';
        tooltipEl.style.left = positionX + tooltip.caretX + 10 + 'px';
        tooltipEl.style.top = positionY + tooltip.caretY - 30 + 'px';
      };

      if (hasData && labels.length > 0 && data.length > 0) {
        new Chart(doughnutChartCanvas, {
          type: 'doughnut',
          data: {
            labels: labels,
            datasets: [{
              data: data,
              backgroundColor: colors,
              borderColor: "#000"
            }]
          },
          options: {
            cutout: 70,
            animationEasing: "easeOutBounce",
            animateRotate: true,
            animateScale: false,
            responsive: true,
            maintainAspectRatio: true,
            showScale: false,
            legend: false,
            plugins: {
              legend: {
                display: false,
              },
              tooltip: {
                enabled: false, // Disable default tooltip
                external: externalTooltipHandler,
                callbacks: {
                  label: function (context) {
                    return `${context.label}: ₹${context.raw.toFixed(2)}`;
                  }
                }
              }
            },
          },
        });
      } else {
        const ctx = doughnutChartCanvas.getContext('2d');
        ctx.font = '16px Arial';
        ctx.textAlign = 'center';
        ctx.fillStyle = '#B0BEC5'; // Light blue-gray for dark mode
        ctx.fillText('No expense data', doughnutChartCanvas.width / 2, doughnutChartCanvas.height / 2);
      }
    }
    if ($('#owl-carousel-basic').length) {
      $('#owl-carousel-basic').owlCarousel({
        loop: true,
        margin: 10,
        dots: false,
        nav: true,
        autoplay: true,
        autoplayTimeout: 4500,
        navText: ["<i class='mdi mdi-chevron-left'></i>", "<i class='mdi mdi-chevron-right'></i>"],
        responsive: {
          0: {
            items: 1
          },
          600: {
            items: 1
          },
          1000: {
            items: 1
          }
        }
      });
    }
    if ($('#audience-map').length) {
      $('#audience-map').vectorMap({
        map: 'world_mill_en',
        backgroundColor: 'transparent',
        panOnDrag: true,
        focusOn: {
          x: 0.5,
          y: 0.5,
          scale: 1,
          animate: true
        },
        series: {
          regions: [{
            scale: ['#3d3c3c', '#f2f2f2'],
            normalizeFunction: 'polynomial',
            values: {

              "BZ": 75.00,
              "US": 56.25,
              "AU": 15.45,
              "GB": 25.00,
              "RO": 10.25,
              "GE": 33.25
            }
          }]
        }
      });
    }
    if ($('#owl-carousel-rtl').length) {
      $('#owl-carousel-rtl').owlCarousel({
        loop: true,
        margin: 10,
        dots: false,
        nav: true,
        rtl: isrtl,
        autoplay: true,
        autoplayTimeout: 4500,
        navText: ["<i class='mdi mdi-chevron-right'></i>", "<i class='mdi mdi-chevron-left'></i>"],
        responsive: {
          0: {
            items: 1
          },
          600: {
            items: 1
          },
          1000: {
            items: 1
          }
        }
      });
    }
    if ($("#currentBalanceCircle").length) {
      var bar = new ProgressBar.Circle(currentBalanceCircle, {
        color: '#ccc',
        // This has to be the same size as the maximum width to
        // prevent clipping
        strokeWidth: 12,
        trailWidth: 12,
        trailColor: '#0d0d0d',
        easing: 'easeInOut',
        duration: 1400,
        text: {
          autoStyleContainer: false,
        },
        from: { color: '#d53f3a', width: 12 },
        to: { color: '#d53f3a', width: 12 },
        // Set default step function for all animate calls
        step: function (state, circle) {
          circle.path.setAttribute('stroke', state.color);
          circle.path.setAttribute('stroke-width', state.width);

          var value = Math.round(circle.value() * 100);
          circle.setText('');

        }
      });

      bar.text.style.fontSize = '1.5rem';

      bar.animate(0.4);  // Number from 0.0 to 1.0
    }
  });
})(jQuery);
