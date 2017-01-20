# -*- coding: utf-8 -*-


#-*- coding: utf-8 -*-



def split_sentence(str):
    if type(str)== type("str"):
        u_str = unicode(str,"utf-8")
        u_result = split_sentence_u(u_str)
        return [s.encode("utf-8") for s in u_result]
    else:
        return split_sentence_u(str)

def split_sentence_u(str):
    # this cannot distinguis dots in the middle of sentence.
    imoticon_chars = [u'ㅎ', u'ㅋ', u'ㄷ', u'ㅠ', u'ㅜ', u'^']

    def is_dot_for_numeric(str, location):
        assert (location != 0 and location < len(str) - 1)

        pre_char = str[location - 1]
        post_char = str[location + 1]
        if pre_char.isdigit() and post_char.isdigit():
            return True
        if pre_char.isspace() and post_char.isdigit():
            return True
        if pre_char.isdigit() and post_char.isspace():
            return True
        return False

    def is_ending_emoticon(str, location):
        if str[location] in imoticon_chars:
            if location +1 == len(str):
                return True

            # Next char is space
            if str[location + 1].isspace():
                return True

            # Next char is also imoticon
            if str[location + 1] in imoticon_chars:
                return True

        return False

    # return is exclusive ( location after imoticon
    def ending_emoticon_end_location(str, location):
        assert (is_ending_emoticon(str, location))
        for i in range(location+1, len(str)):
            if str[i] not in imoticon_chars:
                return i
        return len(str)

    def is_enumerating_dot(str, location):
        pre_char = str[location - 1]
        post_char = str[location + 1]
        if pre_char== '.' or post_char == '.' :
            return False

        st = max(0, location - 4)
        ed = location - 1
        for i in range(st, ed):
            if str[i] == '.':
                return True

        st = location + 2
        ed = min(len(str), location + 5)
        for i in range(location + 1, ed):
            if str[i] == '.':
                return True
        return False

    def is_ending_dot(str, location):
        if str[location] != '.':
            return False
        if location == 0:
            return False
        if location == len(str) - 1:
            return True
        if is_dot_for_numeric(str, location):
            return False
        if is_enumerating_dot(str, location):
            return False
        return True



    delimiter_list = []

    def last_delimiter():
        if delimiter_list :
            return delimiter_list[-1]
        else :
            return -1

    for i, char in enumerate(str):
        if i <= last_delimiter() :
            continue    # Already tested, skip and go on

        if char in ['!', '?', ';']:
            delimiter_list.append(i)

        elif is_ending_dot(str, i):
            delimiter_list.append(i)

        elif is_ending_emoticon(str, i):
            end = ending_emoticon_end_location(str,i)
            for itr in range(i,end):
                delimiter_list.append(itr)

    first_non_delimiters = []
    cursor = 0
    first_non_delimiters.append(cursor)
    for delimiter_loc in delimiter_list:
        if cursor < delimiter_loc:
            first_non_delimiters.append(cursor)
        cursor = delimiter_loc+1
    first_non_delimiters.append(len(str))

    sentences_found = []
    for i,cursor in enumerate(first_non_delimiters[:-1]):
        begin = cursor
        end = first_non_delimiters[i+1]
        sentence = str[begin:end]
        if sentence:
            sentences_found.append(sentence.strip())

    return sentences_found

def test_split_sentence():
    print("Rnning Test for split_sentence...")

    texts = [
            "현기차를 무조건 옹호하는 사람들은 대부분 자동차밥을 먹으며 이해관계가 있거나 지적수준이 좀 떨어지거나.. 머그런거죠ㅎㅎ 저도 현대차 타지만 장점도있는반면 품질수준이하도 함께보여서 객관적이고 공정한 평가를 하는 오너라면 현기차에 대한 절대옹호는 거의 불가능에 가깝죵... 좀 모자라야 가능ㅎㅎ",
            "SM5 단종되지 않을까요?",
             "택시 전용으로 SM5존속시키고 저가형으로 계속 판매...",
             "sm5랑 7을 완전히 단종시키고 6에 올인하는게 차라리 현실 적일듯 합니다. 1월 판매량 보니까 현대 기아 주력차종인 쏘나타 그랜져 반토막 날때 sm5랑 7은 80%가 날라가 버렸어요.. 7 후속 8만들 생각 있다면 7은 존속 시키겠는데 그에 맞는 차종은 르노에는 없죠. 지금 탈리스만으로 라구나 래티튜드 탈리스만이 다 통일 된 건데요. 닛산에서 티아나나 알티마 맥시마 같은 차종 중에 가지고 오면 모르겠는데, 퍽이나 잘도 그럴지..",
             "아방이 빨아서 시급 받으면 됩니다..+_+",
             "100% 입니다..........무조건 현기 판매가 위 입니다 민교압찌 보면 알겠죠",
             "그러고보니 체어맨 충돌테스트 했다는걸 한번도 들어본적이 없네요 ㄷㄷㄷ"
             "현대차 저리 할부는 이미 수년전부터 있었던 걸로 알고 있어요 르노 지엠이 무슨근거로 간신히 유지하는 업체인지는 모르겠습니다. 쌍용이라면 이해가 가도..애시당초 현기 독점으로 인한 국내 소비자 봉 취급 이론을 완성하려면 지엠 르노가 국내시장에서 내수 활성화를 위해 이토록 하고 있어도 현기땜에 안된다는 논리가 완성되야 하는데 그건 또 아니지 않나요? 한국인 현기 봉취급은 지엠 르노도 만만치 않고 애시당초 지엠 르노의 세계시장 점유율이 현기보다 윕니다..설마 현기가 가격정책을 저리 정해서 르노 지엠이 이따구다 라는 이론을 펼치려면 현기가 이 두회사보다 낮은 품질로 높은 가격을 맥인다돈지 동급처량의 가격을 후린다던지가 되야 하는데 건또 아니지 않나요?"
             ]

    for text in texts:
        print("testing:"+ text)
        for s in split_sentence(text):
            print("> " +s)



def is_spam(text):
    strong_spam_keywords = ["몰카", "키스방", "오피", "토토", "건마 ", "풀싸롱", "립카페", "핸플", "ㅂrㅋr"]
    weak_spam_keywords = ["스와핑","엘프녀","회원가입","무료","채팅", "안마", "국산","셀카", "매직미러","op", "야동","만남", "카페", "비아그라","중년여성", "채팅어플", "탈의실", "실시간", "고객", "당일", "상담", "팀장", "인터넷", "현금", "금용", "최저", "입금", "할인", "연체자", "승률", "씨엔조이",
    "비아", "씨알", "환전", "캐피탈", "당첨", "대박", "출현", "잭팟", "섹시", "다빈치", "맞고", "여대생", "출금자", "행진",
    "바카라", "야마토", "가입", "축하", "배지급", "황금성", "대방출", "정글북", "코인", "지급", "카지노", "만원", "확률", "입출금", "머니지급", "방출", "충전", "추급", "빵게판",
    "연타작살", "무료", "육성", "조건", "만남"]

    for keyword in strong_spam_keywords:
        if keyword in text:
            return True

    count = 0
    for keyword in weak_spam_keywords:
        if keyword in text:
            count += 1

    if count > 2 :
        return True

    return False



if __name__ == "__main__":
    test_split_sentence()

