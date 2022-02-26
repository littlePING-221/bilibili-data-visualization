<template>
  <div class="dashboard-container">
    <div id="charts" style="width: 100%; height: 500px"></div>
  </div>
</template>

<script>
import * as echarts from "echarts";
import timeline_data from "./normal_data.json";
export default {
  data() {
    return { myChart };
  },
  mounted() {
    // console.log(testdata.reply);
    this.init();
    window.addEventListener("resize", this.chart_resize);
  },
  methods: {
    init() {
      var chartDom = document.getElementById("charts");
      this.myChart = echarts.init(chartDom);
      var total_options;
      total_options = this.$options.methods.make_total_options(timeline_data);
      console.log(JSON.stringify(total_options));
      this.myChart.setOption(total_options);
    },
    make_total_options(timeline_data) {
      var single_options = [];
      for (var key in timeline_data) {
        /* prettier-ignore */
        single_options.push({
          dataset: {
            dimensions: ["section", "danmaku", "reply", "favorite", "coin", "share", "like"],
            source: timeline_data[key],
          },
          series: Array(6).fill({type:"bar"})
          });
      }
      var total_options = {
        timeline: {
          axisType: "category",
          data: Object.keys(timeline_data),
          playInterval:500,
        },
        legend: {},
        tooltip: {},
        xAxis: {
          type: "category",
        },
        yAxis: {},
        options: single_options,
      };
      return total_options;
    },
  },
  chart_resize() {
    this.myChart.resize();
  },
};
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
</style>
