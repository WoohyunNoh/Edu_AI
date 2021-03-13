<template>
  <div class="text-upload">
    <div class="form-box">
      <button
        class="cancle-btn e-cancle-button no-css-btn"
        style="float: right"
        @click="cancleWrite"
      >
        <i style="color: black" class="fas fa-times fa-2x"></i>
      </button>
      <div class="room-deal-information-container">
        <div class="room-deal-information-title"><h2>Text Input</h2></div>
        <div v-if="texts.length" class="file-preview-content-container">
          <div class="image-box image-box-add">
            <input
              type="text"
              id="text"
              v-model="inputText"
              @keyup.enter="textUpload"
            />
            <button class="confirm-btn btn-b" @click="textUpload">
              등록
            </button>
          </div>
        </div>
        <div class="room-file-upload-wrapper">
          <div v-if="!texts.length" class="room-file-upload-example-container">
            <div class="room-file-upload-example">
              <div class="room-file-image-example-wrapper">
                class에 맞춰 내용을 입력해주세요
              </div>
              <div class="room-file-notice-item room-file-notice-item-red">
                예시) 긍정인 class를 만드신다면 "재밌다", "행복하다" 등의 내용을
                입력해주세요
              </div>
              <div class="room-file-notice-item room-file-upload-button">
                <div class="image-box">
                  <input
                    type="text"
                    id="text"
                    v-model="inputText"
                    @keyup.enter="textUpload"
                  />
                  <button class="confirm-btn btn-a" @click="textUpload">
                    등록
                  </button>
                  <p v-if="$store.state.possample">이대로 저장하셔도 됩니다</p>
                </div>
              </div>
            </div>
          </div>
          <div v-if="texts.length" class="file-preview-content-container">
            <div class="file-preview-container">
              <div
                v-for="(text, index) in texts"
                :key="index"
                class="file-preview-wrapper"
              >
                <div
                  class="file-close-button"
                  @click="removeText"
                  :name="text.number"
                >
                  x
                </div>
                <div>{{ text }}</div>
              </div>
            </div>
            <div class="btn-ok">
              <button @click="comfirm">저장</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {mapGetters, mapMutations} from "vuex";
export default {
  name: "TextUpload",
  props: {
    showInput: Boolean,
    index: Number,
  },
  data() {
    return {
      inputText: "",
      texts: [],
      inputNumber: 0,
    };
  },
  computed: {
    ...mapGetters(["getTextInput", "getTextLength"]),
  },
  created() {
    if (this.index == 0) {
      if (confirm("저희의 긍정 샘플 데이터를 사용해 보시겠어요?")) {
        this.$store.state.possample = true;
        this.$store.getters.getTextInput[this.index].className = "긍정";
        this.$store.getters.getTextInput[this.index].texts = [
          "흠포스터보고 초딩영화줄오버연기조차 가볍지 않구나",
          "사이몬페그의 익살스런 연기가 돋보였던 영화스파이더맨에서 늙어보이기만 했던 커스틴 던스트가 너무나도 이뻐보였다",
          "액션이 없는데도 재미 있는 몇안되는 영화",
          "왜케 평점이 낮은건데 꽤 볼만한데 헐리우드식 화려함에만 너무 길들여져 있나",
          "걍인피니트가짱이다진짜짱이다",
          "볼때마다 눈물나서 죽겠다년대의 향수자극허진호는 감성절제멜로의 달인이다",
          "담백하고 깔끔해서 좋다 신문기사로만 보다 보면 자꾸 잊어버린다 그들도 사람이었다는 것을",
          "ㄱ냥 매번 긴장되고 재밋음ㅠㅠ",
          "참 사람들 웃긴게 바스코가 이기면 락스코라고 까고바비가 이기면 아이돌이라고 깐다그냥 까고싶어서 안달난것처럼 보인다",
          "이건 정말 깨알 캐스팅과 질퍽하지않은 산뜻한 내용구성이 잘 버무러진 깨알일드",
          "약탈자를 위한 변명 이라 저놈들은 착한놈들 절대 아닌걸요",
          "나름 심오한 뜻도 있는 듯 그냥 학생이 선생과 놀아나는 영화는 절대 아님",
          "보면서 웃지 않는 건 불가능하다",
          "절대 평범한 영화가 아닌 수작이라는걸 말씀드립니다",
          " 고추를 털어버려야 할텐데",
          "재밋는뎅",
          "센스있는 연출력탁월한 캐스팅년대의 향수 그래서 점",
          "엄포스의 위력을 다시 한번 깨닫게 해준 적남 꽃검사님도 연기 정말 좋았어요 완전 명품드라마",
          "재밌는데 별점이 왜이리 낮은고",
          "아직도 이 드라마는 내인생의 최고",
          "패션에 대한 열정 안나 윈투어",
          "허허원작가 정신나간 유령이라 재미있겠네요",
          "이 영화가 왜 이렇게 저평가 받는지 모르겠다",
          "광장한 작품 옛날것도 보고 싶다",
          "내 생의 최고의 영화",
          "어린시절 너무 무섭고 재미있게 봤던 추억의 판타지영화절대 나쁜짓은 금물지옥가요",
          "난 사랑비 서준에게 쏙 빠져버렸네 초만에 쏙ㅋㅋ난 절대잊지도않고후회도안할거야",
          "이영화를보니까 교훈을 주네요 나도 남은인생을 화려하게 살아야겟다 말밖에 안나오네요",
          "나름 추억에 젖어들고 좋았음ㅋㅋ아무생각없이 가볍게 보고오기 추천요",
          "단순한 싸이코물을 벗어난",
          "넘 사랑스러운 영화다 ㅠㅠ 보고  연이어 봤다 넘 귀여워 ㅠㅠ",
          "청춘 영화만이 줄 수 있는 감성이 넘쳐난다 이 순간 지나가면 다시 돌아오지 않을테지만 그 순간만큼은 무한할 젊음이 줄 수 있는 그런 감성",
          "용 건담 시리즈 중에서 아직까지도 최고봉",
          "사다코의 한이 서린 우물펀치ㅜㅜ 감동",
          "아정말 김혜성 너무 예쁘네요 이현진도 웃는 거 정말하",
          "화려한여정이인상깊어요ㅋㅋ재밋어요ㅋㅋ배두나연기정말잘해요ㅋ",
          "감동적인 영화",
          "이건 말이 필요 없다 그냥 닥치고 봐라",
          "각기 다른 사람들의 재밌고 멋진 사랑영화",
          "역시 미국드라마의 파워 정말 알수없는 그 미묘함까지 사로잡아버렸다 최고",
          "너무너무 훈훈하네요",
          "아 너무 웃기고 배꼽 빠질뻔했네 내 컴에 이 영화 있는데",
          "작은거 하나에도 설레어했던 학창시절 그때 그느낌을 다시 느껴볼수있는시간이었다 장면 하나 하나 대사 하나 하나 배경음악 하나 하나 버릴게 없는 드라마",
          "이승기 정말 연기 잘하는 조연들도 연기 정말 잘하고",
          "현실은 꿈 꿈은 현실",
          "오늘 현충일특집프로로 보게되었습니다 년도의 매우 훌륭한 작품입니다",
          "제대하고 보니까 더 재밌네요 ㅋㅋㅋㅋ",
          "영화를 보는것만으로도 마음의 휴가를 다녀온 느낌소박하지고 잔잔하지만 지루하지않은그래서 다시 보고싶은 영화햇살가득한 비이의 부엌과 요리도 인상적",
          "년 그때 당시에는 우리 나라에 이런 판타지 로맨스가 없었다 아직도 신현준의 황장군 연기는 음 괜찮네 ㅎㅎ한석규의 전성시대가 열린 영화 이때 한석규한테 뿅 갔었다",
          "일단 재생하면 괴물같은 서스펜스 귀신같은 흡입력",
          "어떻게 이런 상상을 대단하다",
          "세계최초의 반공 애니매이션이라는 역사적 가치가 있다",
          "감각적인시각으로바라보는색다른느낌의사랑문학적이",
          "그저 한마디뿐 알리시아",
          "진짜 생생하게 느낄 수 있었다",
          "재밌는데 평점이 이상하다 싶을 정도로 낮다",
          "드라마 너무 재밓당",
          "아진짜너무좋아요ㅜㅜ짱짱",
          "연기 굿",
          "이런 영화 다시는 안나오겠지그때 시절을 잘나타내주었던거같아요 ㅎㅎ",
          "중간정도 부터 봤는데도 꽤나 대단하군요",
          "뭔가알수없는매력에빠져드는 영화",
          "재밌는데 평점이 왜 이렇게 구리지",
          "또보고 싶은데 어디서 보죠",
          "영화 재미있드만 ㅎㅎ",
          "좋은영화",
          "년 전에 봐서 기억이 나질 않지만 진개가천카이거 감독 이름 세 자는 기억해 두었던",
          "정은지 언니 연기 잘하구노래도 잘부르시고 마지막회 웃으면서 즐겁게 봤습니다 트로트의 연인",
          "아이의 시선으로 보는 전쟁 보는 내내 가슴이 먹먹했다는",
          "설정이 연속극같은 느낌이 든다 하지만 배우들의 연기가 뛰어나다",
          "또 보고 또 울었다",
        ];
      }
    }
    if (this.index == 1) {
      if (confirm("저희의 부정 샘플 데이터를 사용해 보시겠어요?")) {
        this.$store.state.navsample = true;
        this.$store.getters.getTextInput[this.index].className = "부정";
        this.$store.getters.getTextInput[this.index].texts = [
          " 전기세가 아까웠던 영화다",
          "이배우들가지고이러면안돼 스토리 얼개가 다인 영화",
          "그냥 말할필요가없네",
          "이건 별 주기도 아까운데 구성이며 스토리며 대단한 소재로 쓰레기를 만든 첸카이거",
          "안타깝지만 최악은 아니다",
          "감정표현은 좋았는데 뭔 내용인지",
          "이게 년 한국영화 블록버스터였다니",
          "뭐냐이쓰레기는",
          "아 진짜 우리나라 이런 류영화 좀 만들지 마라 헐리우드 따라할려면 좀 제대로 따라하던가 머냐 이게 ㅡㅡ",
          "확실히 기대 이하 어느정도 예상 가능한 결말에 정말 공포라고 느낄 부분이 없음일본 박스오피스 주간 위 주인공이 아이돌이라 그런가 보네",
          "무슨 생각으로 이런 진부한 스토리를 갖고 영화를 만들었으며 돈까지 받아 먹는걸까",
          "점주는것도 후회하지 않아",
          "망했어 이건",
          "역시 이순재 할아버지가 나와야돼ㅋㅋ감자별은 재밌음ㅋㅋ",
          "중요한건 여주가 너무 연기못함 아이고 책을 읽는구나",
          "왠만하면 참고 보는데 이건 너무한다",
          "편에서 끝났어야 했다",
          " 점도 아까움 도대체 박헤미 같은 실력파가 왜 이런 쓰레기 영화를 찍었는지",
          "ㅎㅎㅎ극본대로최선을 다해 연기하는 배우분들이 불쌍해보입디다근데 하나하나 말도안되는어거지설정에도 끝 또한 뻔한결과란걸 알면서도욕하면서 시청하고있는 국민들이 더 불쌍하네요ㅎ왠만큼질떨어지는 프로를봐도 그려려니지나쳤는데평점까지 쓰니",
          "어제 이 영화 봤다 근데 어떻게 만장일치로 점이냐 동참",
          "드라마를 좋아해서 딱히 그시간대 볼것없어 틀어놓긴하는데 제발 진도좀 나가자구요ㅜㅜ",
          "시험지만 보면 기역이 안나요 머드라 꿈의 시험이 시작된다",
          "생동감을 다잃어버린 짜집기",
          "이걸 영화라고 만든겁니까",
          "한국포스터엔 세븐을 언급하는 카피라이트가 있었던거 같은데 그래서 더 실망",
          "평점조절 필요",
          "죄없는 선생만 불쌍하네",
          "와나 알바제대로풀었네 존나오글거려서 한번보고실패하고 두번보고또실패한영화인데",
          "이걸 이제야 쓰네ㅋㅋㅋㅋ그냥그런대로 본것같은데 별로재미까지는모르겠다",
          "너무 너무 잘 베끼는구먼",
          "뭔지 몰라도 무관심에 최절정이네 ㅋㅋ 참여인원명 ㅋㅋㅋ",
          "이거 시청률 높네요 인줄 알았는데 까지도 나왔었네요ㄷㄷ 누가 보는거지",
          "김 얼굴 웃겨서 그나마 점 준다",
          "뭐래냐 영상미빼곤 볼거없는 영화",
          "판타지 미스터리 스릴러 장르는 화려하다",
          "뭔 다큐멘타리인가 성에 목마른 짐승들의 전주곡인가",
          "그래서 해외입양이 왜 나쁜걸까요",
          "점도 아깝네",
          "제목 베끼지좀 말아라 명작 만화랑 똑같네",
          "크리스마스에 영화중에 가장 지루한 영화 산타와 요정들이 선물갔다주는 장면 말로 흥미를 끄는 장면이 없고 너무 인물들의 심리에 초점을 두고 있어 좀 지루함  아이들이 보기에는 너무 현실적이고 어른들이 보기에는 너무 지루한 어중간한 영화 개인생각",
          "더 데이 검색하니 뭐 이런 거지같은게 나오나 점 먹어라",
          "밋밋한 대화어정쩡한 케릭터뻔한 스토리",
          "마지막에 재미있었습니다",
          "송은희 게짱난다 게시끄럽네",
          "난 왜 이 영화를 보다가 잤을까",
          "머시여",
          "삶의 방식이 다른것도 전혀 공감안되고 재미없는게 최악",
          "동건이형도 많이 후회하고있겠지",
          "하나경씨보는내내안타까웠음배역도성상납해서받는것같구갠적생각처음그콧수염아저씨랑섹스할때그냥안타깝단느낌ㅠㅠ콧수염아저씨가만지는데ㅠㅠ이런영화는보여주려는게무엇인지모르겠음ㅠ",
          "으휴이건 또 뭐냐 할말이없다",
          "왜 마이너스는 없는걸까 하다못해 다음처럼 점이라도 만들어주세요ㅋㅋㅋㅋ",
          "허경영이 영화감독을 한다면 이럴 듯",
          "촬영지 하나 기억에 남네절경이로다",
          "친구가 나한테 이거 재밋다고 이빨까서 여자친구랑 둘이 보러갔다가 영화끝나고 쫒아가서 아구창 찢어놓을뻔",
          "제시카 알바때문에 그나마 점",
          "중반부터 지루해지네",
          "정말 무섭게도 실제 이야기의 주인공들은 대부분 보호관찰 처분만을 받았습니다 년 산 애 명 빼고 미국 사이트에서는 이들이 빈민가의 흑인이었다면 오지게 살고나왔으리리고들 합니다 실제 이들은 현재 다수가 블로그 등으로 유명인 행세하며 떳떳해 합니다",
          "독립영화계에 최악의 영화 지루하다 정말 지루하다",
          "이거 나올때 친구랑로 같이봤는데 분정도보고 삭제",
          "제목만 웃긴듯",
          "천재는 만들어진다",
          "인어아가씨오로라공주를 섞은것같네요 내용이 이러다 신기생던처럼 귀신도 나올것같은데요막장막장 하면서도 보게돼네요 그래도",
          "내 영화비 내놔  아근데 여기에 에드워드 노튼나오더라 기가막히네",
          "한국사람으로 부터 바이러스가 전파된것 마냥 그려지는게 좀 불쾌했던 영화",
          "폭발보고 하루종일 웃었다 아직도 생각나면 웃긴닼ㅋㅋㅋㅋㅋㅋㅋㅋㅋ",
          "카메라맨이 헛구역질할때 그장면이 꼭 필요한가 카메라맨이 씨씨티비로본 그장면은 리얼인가 환영인가 리얼이라면 홀려서 그런행동을했을까 아니면 원래 성향이그래서 자발적으로 한 것인가 하는 의문따윈 사치인 영화 그리고 마지막은 뜬금포다 ㅡㅡ",
          "다 봤는데 아무 재미도 없고 의미도 없습니다 싸이코풍만 잔뜩 넣어놓고 재미는 하나도 없습니다 다 보고나서 영 찜찜 하기만하고 급영화에요 왜 평점이 점씩이나 돼서 사람을 낚는지 모르겠네요",
          NaN,
          "내가 감독을 죽이러 가고 싶을 정도의 생각이 들었다",
          "오스틴은 그렇다치고다른 배우들은 왜 발연기를ㅜㅠ",
          "재미도 하나 없구만뭐이리 평점이 높아",
          "시상에이런 괴물같은걸세상에 내놓다니",
          "이 쓰레기 어디다 버리면되나요",
          "극장판은 기네 ㅋ 거기에에비하면 는 정말훌륭한거야 ㅋ",
          "심하게 지겨웠음 ",
          "이건 무슨 잔인함의 극치임 무슨영화가 끝까자 질질끌고가냐",
          "어린 아역배우 에게 왜 칼과도끼를쓰는 살인킬러 연기를 시켰는지 도저히 이해가안감",
          "연출을 발로 한 영화 짜증 남",
          "분 정도로 만들었으면 좋았을 영화 시간은 인내심의 한계에 도달하게 만든다 등장인물 명에 아무 상돤도 없는 중간에 나오는 옆집부부 고양이 한마리 분 정도 했으면 여운이 남았을거 같은데 엔딩도 여운을 남기기엔 너무 긴 플레잉 타임",
          "어유 유치해라 봭 막장임 점도 아깝다",
          "감독이 아는척을 하고 싶어 하는것 같다 하지만 그에게 편집의 기술이 없다",
          "굉장히지루하게봄",
          "아당했다 ㅜㅜ",
          "원작의 어설픈 변형과 미스 캐스팅결과는 제작비의 절반만 벌어들임",
          "진짜 딸인거 밝혀질때부터 볼까봐요",
          "그냥 자위 야동 이상 이하도 아님 내가 보수적인가 딴에는 물론 예술영화 라고 만들었겠지만 보고나서 기분 찜찜하고 더러운 느낌은 뭘까 얼마전 낸시랭 지하철에서 신음소리 퍼포먼스도 그렇고 도덕적 윤리의 금기와 예술의 선이 뭘까",
          "현실적으로 이런일을 벌어질수없지 않을까 싶어요일도 해내고 유혹도 이겨내고 가정도 지키는저런 여자가 어딧어요",
          "이유없이 악평을 받았던게 아니었다",
          " 왤케 큼 지금 에서 떡치고 있음 시 분임 ㅋㅋㅋㅋㅋㅋㅋㅋㅋ",
          "애국심에 기대려는 상업적 꼼수가 너무 드러나는 영화",
          "그냥 포르노영화수준 여배우들 아니 전체 배우들의 연기는 그냥 동네학예회수준연출도 급아니 급이다 그냥 포르노보고싶으신 분들은 이거 보시는걸 추천할정도로 배드신빼고는 기억에 하나도 안남는다 마지막 복수장면 배우들의 발연기는 가관이였다 진짜",
          "지나치게 저학년 연령층만 주 시청자층으로 설정하고 있는 애니",
          "영화가 이야기하는건 어벤져스를 안 보고 이걸를 본 나를 나무라는것같다 개같은 나무들",
          "내가본 최악의 중 하나다이걸왜봤을까 차라리 볼시간에 부족한잠이라도 잘껄 후회된다",
          "보면서 잤다는이렇게 잼 없고 어수선한 만화영화는 처음",
          "무엇을 이야기하려는 줄은 알겠지만 전개도 너무 느리고 리얼한 맛이 좀 떨어진다 가족간에 싸울때도 그렇고 그냥 조용조용하게 만 한다대사도 아주 천천히 작게 말하고",
          "유덕화 등 홍콩 배우들은 단역이고 왠 중국계 미국애들이 주인공임 이게 실화라니",
          "김기덕 정말 좋아하는데 이 영화는 그지 같아요 본 김기덕 중 최하",
          "같은 영화다",
          "함량 미달 자체를 즐기라 애교로 뭉친 삼총녀의 황홀증 탐구를",
          "돈날렸다 공감좀ㅋㅋ",
          "본인은 이 영화에 대해 그럭저럭 볼만하다는 반응을 나타내었다",
        ];
      }
    }

    this.texts = this.getTextInput[this.index].texts;
  },

  mounted() {
    // this.texts = this.getTextInput[this.index].texts;
  },
  methods: {
    ...mapMutations(["deleteText"]),
    comfirm() {
      this.getTextInput[this.index].texts = this.texts;
      console.log("18", this.getTextInput[this.index]);
      this.$emit("modal-show");
    },
    cancleWrite() {
      this.$emit("modal-show");
    },
    textUpload() {
      //하나의 배열로 넣기
      if (this.inputText.length != 0) {
        this.texts = [
          ...this.texts,
          {
            text: this.inputText,
            number: this.inputNumber++,
          },
        ];
        this.inputText = "";
      } else {
        alert("한 글자 이상 입력해 주세요.");
      }
    },
    removeText(e) {
      let name = e.target.getAttribute("name");
      this.texts = this.texts.filter((data) => {
        return data.number !== Number(name);
      });
    },
  },
};
</script>

<style scoped>
/* 전체화면영역 */
.text-upload {
  /* display: flex; */
  width: 100%;
  height: 100%;
  left: 0;
  top: 0;
  position: fixed;
  z-index: 9999;
  background: rgba(0, 0, 0, 0.5);
  transition: 0.5s;
  /* position: relative; */
}
.form-box {
  border-radius: 5px;
  position: absolute;
  /* 정가운데 정렬 */
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 40%;
  height: 80%;
  background: white;
  margin: 0 auto;
}
.room-deal-information-container {
  /* display: flex; */
  margin-top: 50px;
  color: #222222;
}

.room-deal-information-title {
  text-align: center;
  font-size: 18px;
  line-height: 60px;
}

.room-deal-information-content-wrapper {
  min-height: 50px;
  display: flex;
}

.room-deal-informtaion-content-title {
  font-size: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 150px;
  background-color: #f9f9f9;
}

.room-deal-information-content {
  width: 100%;
  font-size: 14px;
}

.room-deal-option-selector {
  display: flex;
  align-items: center;
  padding: 15px;
}

.room-deal-option-item {
  width: 100px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #cccccc;
  border-radius: 5px;
  cursor: pointer;
}

.room-deal-option-item:last-child {
  margin-left: 10px;
}

.room-deal-option-notice {
  margin-left: auto;
  font-size: 14px;
  color: #888888;
}

.room-deal-option-item-deposit {
  margin-left: 10px;
}

.room-deal-information-wrapper {
  display: flex;
  flex-direction: column;
}

.room-deal-information-option {
  padding: 10px;
  display: flex;
  align-items: center;
}

.room-deal-information-option:last-child {
  border-bottom: 1px solid #dddddd;
}

.room-deal-information-item-type {
  font-size: 13px;
  color: #fff;
  background-color: #61b6e5;
  min-width: 50px;
  height: 26px;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 3px;
}

.room-deal-information-item-wrapper {
  display: flex;
  align-items: center;
  margin-left: 10px;
  height: 46px;
  width: 100%;
}

.room-deal-information-item-wrapper > input {
  border: 1px solid #dddddd;
  width: 140px;
  height: 100%;
  padding: 0 15px;
  font-size: 15px;
}

.room-deal-inforamtion-won {
  margin: 0 10px;
}

.room-deal-information-example {
  color: #888888;
}

.room-deal-information-option:not(:first-child) {
  margin-top: 10px;
}

.room-deal-inforamtion-divide {
  font-size: 22px;
  margin: 0 8px;
  color: #222222;
  font-weight: 100;
}

.room-deal-close-button-wrapper {
  margin-left: auto;
  cursor: pointer;
}

.room-deal-close-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  background-color: #666666;
  color: rgb(220, 220, 220);
}

.room-deal-cliked {
  background-color: rgb(235, 235, 235);
  color: rgb(170, 170, 170);
}

.room-file-upload-example {
  height: 100%;
}

.room-write-content-container {
  border-top: 1px solid #dddddd;
  min-height: 260px;
}

.room-picture-notice {
  margin: 20px;
  padding: 20px 40px;
  border: 1px solid #dddddd;
}

.file-preview-content-container {
  height: 100%;
}

.room-file-upload-wrapper {
  overflow-y: auto;
  margin: 30px;
  border: 1px solid #dddddd;
  background-color: #f4f4f4;
  min-height: 300px;
  font-size: 15px;
  color: #888888;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 300px;
  border-radius: 10px;
}

.room-file-upload-wrapper::-webkit-scrollbar {
  width: 0px;
  background: none;
  border-radius: 5px;
}
.room-file-upload-wrapper::-webkit-scrollbar-thumb {
  background-color: none;
}
.room-file-upload-wrapper::-webkit-scrollbar-track {
  background-color: none;
}

.room-file-upload-example-container {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 50px;
}

.room-file-image-example-wrapper {
  text-align: center;
}

.room-file-notice-item {
  margin-top: 5px;
  text-align: center;
}

.room-file-notice-item-red {
  color: #6383eb;
}

.image-box {
  margin-top: 30px;
  padding-bottom: 20px;
  text-align: center;
}

.image-box input[type="text"] {
  /* position: absolute; */
  left: 50px;
  padding: 10px;
  border-radius: 5px;
  width: 65%;
  border: 2px solid rgba(128, 128, 128, 0.267);
}

.image-box input:focus {
  outline: none !important;
  border: 0;
  box-shadow: 5px 5px 9px 1px gray;
}

.image-box .confirm-btn {
  display: inline-block;
  background-color: #b1bfeb;
  color: #fff;
  vertical-align: middle;
  font-size: 15px;
  cursor: pointer;
  border-radius: 5px;
  margin-left: 10px;
  font-weight: 700;
  border: none;
}
.btn-a {
  padding: 10px 20px;
}
.btn-b {
  height: 35px;
  width: 60px;
}
.image-box-add {
  flex-direction: row;
  margin-left: 10px;
}
.image-box-add input {
  height: 30%;
  width: 300px;
}
.file-preview-wrapper {
  background: rgba(144, 198, 241, 0.63);
  border-bottom: 1px solid rgb(214, 214, 214);
  height: auto;
  padding: 10px;
  position: relative;
  overflow-y: auto;
  color: whitesmoke;
  font-weight: 700;
}

.file-close-button {
  position: absolute;
  /* align-items: center; */
  line-height: 18px;
  z-index: 99;
  font-size: 18px;
  right: 0px;
  top: 0px;
  color: #fff;
  font-weight: bold;
  background-color: #666666;
  width: 20px;
  height: 20px;
  text-align: center;
  cursor: pointer;
}

.file-preview-container {
  width: 552px;
  /* height: 100%; */
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
}

.file-preview-wrapper-upload {
  margin: 10px;
  padding-bottom: 20px;
  /* background-color: #888888; */
  width: 120px;
  height: 100px;
}

.room-write-button-wrapper {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #222222;
}

.room-write-button-wrapper > div {
  width: 160px;
  height: 50px;
  border: 1px solid #dddddd;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 15px;
  cursor: pointer;
}

.room-write-button {
  margin-left: 15px;
  color: #fff;
  background-color: #b1bfeb;
}

.room-write-button:hover {
  opacity: 0.8;
}
.cancle-btn {
  background: none;
  border: none;
  padding: 15px;
  position: absolute;
  right: 0;
  margin-right: 5px;
}
.btn-ok {
  position: absolute;
  bottom: 10px;
  left: 43%;
  text-align: center;
  margin: 10px;
}
.btn-ok > button {
  padding: 10px;
  width: 80px;
  border-radius: 5px;
  background-color: #b1bfeb;
  border: none;
  font-weight: 700;
  color: white;
}
.textname {
  text-align: center;
}
</style>
