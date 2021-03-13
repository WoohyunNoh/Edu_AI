<template>
  <div class="imagethree">
    <div class="carousel-wrapper">
      <span id="image-1"></span>
      <span id="image-2"></span>
      <span id="image-3"></span>
      <span id="image-4"></span>
      <div class="carousel-image image-1">
        <h2>이미지 3</h2>
        <p>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus
          accumsan pretium dolor vel convallis. Aliquam erat volutpat. Maecenas
          lacus nunc, imperdiet sed mi et, finibus suscipit mi.
        </p>
        <a class="arrow arrow-prev" href="#image-4"></a>
        <a class="arrow arrow-next" href="#image-2"></a>
      </div>

      <div class="carousel-image image-2">
        <h2>Text 2</h2>
        <p>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus
          accumsan pretium dolor vel convallis. Aliquam erat volutpat.
        </p>
        <a class="arrow arrow-prev" href="#image-1"></a>
        <a class="arrow arrow-next" href="#image-3"></a>
      </div>

      <div class="carousel-image image-3">
        <h2>Text 3</h2>
        <p>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus
          accumsan pretium dolor vel convallis. Aliquam erat volutpat.
        </p>
        <a class="arrow arrow-prev" href="#image-2"></a>
        <a class="arrow arrow-next" href="#image-4"></a>
      </div>

      <div class="carousel-image image-4">
        <h2>Text 4</h2>
        <p>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus
          accumsan pretium dolor vel convallis. Aliquam erat volutpat.
        </p>
        <a class="arrow arrow-prev" href="#image-3"></a>
        <a class="arrow arrow-next" href="#image-1"></a>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "imagethree",
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
.carousel-image {
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
[id^="image"] {
  display: none;
}

.image-1 {
  z-index: 2;
  opacity: 1;
  background: url("https://static.pexels.com/photos/6526/sea-beach-holiday-vacation-large.jpg");
  background-size: cover;
}
.image-2 {
  background: url("https://static.pexels.com/photos/6506/alcohol-bar-drinks-party-large.jpg");
  background-size: cover;
}
.image-3 {
  background: url("https://static.pexels.com/photos/6529/lake-kajak-kayak-large.jpg");
  background-size: cover;
}
.image-4 {
  background: url("https://static.pexels.com/photos/6529/lake-kajak-kayak-large.jpg");
  background-size: cover;
}

*:target ~ .image-1 {
  opacity: 0;
}

#image-1:target ~ .image-1 {
  opacity: 1;
}

#image-2:target ~ .image-2,
#image-3:target ~ .image-3,
#image-4:target ~ .image-4 {
  z-index: 3;
  opacity: 1;
}
</style>
