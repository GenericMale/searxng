/* SPDX-License-Identifier: AGPL-3.0-or-later */
(function (w, d, searxng) {
  'use strict';

  if (searxng.endpoint !== 'results') {
    return;
  }

  searxng.ready(function () {
    function showServerTimings (entryList, observer) {
      observer.disconnect();

      const table = document.querySelector('#engines_msg-table');
      const serverTiming = entryList.getEntries().reduce((a, e) => a.concat(e.serverTiming), []);
      if (!table || serverTiming.length === 0) {
        return;
      }

      const total = serverTiming.find(e => e.name === 'total');
      serverTiming.filter(t => t.name.startsWith('total_')).forEach(timing => {
        const name = timing.name.split('_').pop();
        const bar = Math.round(100 * timing.duration / total.duration);
        table.insertAdjacentHTML('beforeend', `
        <tr>
            <td class="engine-name">
                <a href="./stats?engine=${name}">${name}</a>
            </td>
            <td class="response-time">
                <div class="bar-chart-value">${(timing.duration / 1000).toFixed(1)}</div>
                <div class="bar-chart-graph">
                    <div class="bar-chart-serie1 bar${bar}"></div>
                </div>
            </td>
        </tr>`);
      });
    }

    const observer = new PerformanceObserver(showServerTimings);
    observer.observe({type: "navigation", buffered: true});
  });
})(window, document, window.searxng);
