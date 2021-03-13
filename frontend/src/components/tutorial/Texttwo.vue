<template>
  <div class="texttwo">
    <div class="carousel-wrapper">
      <span id="text-1"></span>
      <span id="text-2"></span>
      <span id="text-3"></span>
      <span id="text-4"></span>
      <div class="carousel-text text-1">
        <h2>튜토리얼 2</h2>
        <p>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus
          accumsan pretium dolor vel convallis. Aliquam erat volutpat. Maecenas
          lacus nunc, imperdiet sed mi et, finibus suscipit mi.
        </p>
        <a class="arrow arrow-prev" href="#text-4"></a>
        <a class="arrow arrow-next" href="#text-2"></a>
      </div>

      <div class="carousel-text text-2">
        <h2>Text 2</h2>
        <p>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus
          accumsan pretium dolor vel convallis. Aliquam erat volutpat.
        </p>
        <a class="arrow arrow-prev" href="#text-1"></a>
        <a class="arrow arrow-next" href="#text-3"></a>
      </div>

      <div class="carousel-text text-3">
        <h2>Text 3</h2>
        <p>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus
          accumsan pretium dolor vel convallis. Aliquam erat volutpat.
        </p>
        <a class="arrow arrow-prev" href="#text-2"></a>
        <a class="arrow arrow-next" href="#text-4"></a>
      </div>

      <div class="carousel-text text-4">
        <h2>Text 4</h2>
        <p>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus
          accumsan pretium dolor vel convallis. Aliquam erat volutpat.
        </p>
        <a class="arrow arrow-prev" href="#text-3"></a>
        <a class="arrow arrow-next" href="#text-1"></a>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "texttwo",
  data() {
    return {};
  },
  methods: {},
};
</script>

<style scoped>
.carousel-wrapper {
  height: 468px;
  position: relative;
  width: 832px;
  margin: 0 auto;
}
.carousel-text {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 25px 50px;
  opacity: 0;
  transition: all 0.5s ease-in-out;
}
.arrow {
  border: solid black;
  border-width: 0 3px 3px 0;
  display: inline-block;
  padding: 12px;
}

.arrow-prev {
  left: -30px;
  position: absolute;
  top: 50%;
  transform: translateY(-50%) rotate(135deg);
}

.arrow-next {
  right: -30px;
  position: absolute;
  top: 50%;
  transform: translateY(-50%) rotate(-45deg);
}

.light {
  color: white;
}

@media (max-width: 480px) {
  .arrow,
  .light .arrow {
    background-size: 10px;
    background-position: 10px 50%;
  }
}

/*Select every element*/
[id^="text"] {
  display: none;
}

.text-1 {
  z-index: 2;
  opacity: 1;
  background: url("https://static.pexels.com/photos/6526/sea-beach-holiday-vacation-large.jpg");
  background-size: cover;
}
.text-2 {
  background: url("https://static.pexels.com/photos/6506/alcohol-bar-drinks-party-large.jpg");
  background-size: cover;
}
.text-3 {
  background: url("https://static.pexels.com/photos/6529/lake-kajak-kayak-large.jpg");
  background-size: cover;
}
.text-4 {
  background: url("https://static.pexels.com/photos/6529/lake-kajak-kayak-large.jpg");
  background-size: cover;
}

*:target ~ .text-1 {
  opacity: 0;
}

#text-1:target ~ .text-1 {
  opacity: 1;
}

#text-2:target ~ .text-2,
#text-3:target ~ .text-3,
#text-4:target ~ .text-4 {
  z-index: 3;
  opacity: 1;
}
</style>
