<template>
  <div class="app-container" style="display: flex">
    <meta name="referrer" content="no-referrer" />
    <!-- <img src="http://i2.hdslb.com/bfs/archive/1e683a5363f35aa0a65419dbf145177099e38f90.jpg"/> -->
    <div id="charts" style="margin: 0 50px; width: 700px; height: 600px" />
    <div>
      <el-checkbox-group
        v-model="selected"
        style="padding: 70px 0; width: 70px"
        :max="2"
        @change="bindCheckbox"
      >
        <!-- prettier-ignore -->
        <el-checkbox v-for="column in this.columns" :label="column" :key="column" style="margin: 0; width:100px" border>
          {{ column }}
        </el-checkbox>
      </el-checkbox-group>
    </div>
  </div>
</template>

<script>
import * as echarts from "echarts";
import scatter_data from "./scatter_data.json";
export default {
  data() {
    return {
      myChart: [],
      option: {},
      x: 0,
      y: 1,
      /* prettier-ignore */
      columns:['时长', '播放量', '弹幕', '回复', '收藏', '投币', '分享','点赞'],
      selected: ["时长", "播放量"],
    };
  },
  mounted() {
    this.init();
    window.addEventListener("resize", this.chart_resize);
  },
  methods: {
    init() {
      var chartDom = document.getElementById("charts");
      this.myChart = echarts.init(chartDom);
      this.option = this.$options.methods.make_option(this.x, this.y);
      // console.log(JSON.stringify(this.option));
      this.myChart.setOption(this.option);
      this.myChart.on("click", (params) => {
        // console.log(params.data[4]);
        window.open("https://www.bilibili.com/video/" + params.data[4]);
      });
    },
    make_option(x, y) {
      // console.log(JSON.stringify(mydata));
      /* prettier-ignore */
      var columns=['时长', '播放量', '弹幕', '回复', '收藏', '投币', '分享','点赞']
      var option = {
        color: [
          "#5470c6",
          "#91cc75",
          "#fac858",
          "#ee6666",
          "#73c0de",
          "#3ba272",
          "#fc8452",
          "#9a60b4",
          "#ea7ccc",
          "#516b91",
          "#59c4e6",
          "#edafda",
          "#93b7e3",
          "#a5e7f0",
        ],
        /* prettier-ignore */
        legend: {
          selector: ['all', 'inverse'],
          width:500,
          data:["动画", "音乐", "舞蹈", "游戏", "知识", "数码", "汽车", "生活", "美食", "动物圈", "鬼畜", "时尚", "娱乐", "影视"],
          textStyle:{
            fontSize:16
          }
        },
        xAxis: {
          name: columns[x],
          nameLocation: "center",
          nameTextStyle: {
            padding: 4,
            fontSize: 18,
          },
        },
        yAxis: {
          name: columns[y],
          nameRotate: 90,
          nameLocation: "center",
          nameTextStyle: {
            fontSize: 18,
          },
        },
        visualMap: [
          {
            min: 1,
            max: 100,
            right: 30,
            top: 50,
            itemWidth: 50,
            dimension: 5,
            text: ["排名     "],
            handleSize: "130%",
            indicatorSize: "30%",
            inverse: true,
            textStyle: { fontSize: 18 },
            // precision: 1,
            range: [1, 100],
            inRange: {
              symbolSize: [20, 5],
            },
            calculable: true,
          },
        ],
        dataZoom: [
          {
            type: "slider",
            xAxisIndex: [0],
            bottom: "1%",
          },
          {
            // left: 630,
            type: "slider",
            yAxisIndex: [0],
          },
          // {
          //   type: "inside",
          //   xAxisIndex: [0],
          //   yAxisIndex: [0],
          // },
        ],
        tooltip: {
          show: true,
          trigger: "item",
          formatter: (params) => {
            let title = "";
            for (let i = 0; i < params.value[2].length; i += 18) {
              title += params.value[2].substr(i, 18);
              title += "\n";
            }
            console.log(title);
            /* prettier-ignore */
            let ret =
              "<div>(" +
                params.value.slice(0, 2) +
              ")</div>" +
              "<div style='white-space: pre-line'>" +
                title +
              "</div>" +
              "<img style='width:250px;height:150px' src='" +
                params.value[3] +
              "' />";
            // console.log(ret);
            return ret;
          },
        },
        series: [],
      };
      // make series data
      for (var key in scatter_data) {
        // console.log(key)
        var mydata = [];
        var section_data = scatter_data[key];
        // console.log(JSON.stringify(section_data))
        for (var i of section_data) {
          var tmp = [];
          tmp.push(i[x]);
          tmp.push(i[y]);
          tmp.push(i[9]); // title
          tmp.push(i[10]); // img link
          tmp.push(i[11]); // BV https://www.bilibili.com/video/{BV}
          tmp.push(i[12]); // rank

          mydata.push(tmp);
        }
        // console.log(JSON.stringify(mydata))
        option.series.push({
          name: key,
          type: "scatter",
          data: mydata,
          symbolSize: 10,
        });
      }
      return option;
    },
    bindCheckbox() {
      if (this.selected.length == 2) {
        this.x = this.columns.indexOf(this.selected[0]);
        this.y = this.columns.indexOf(this.selected[1]);
        this.option = this.$options.methods.make_option(this.x, this.y);
        this.myChart.setOption(this.option);
      }
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
