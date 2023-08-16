import streamlit as st
import requests
import time
from PIL import Image
import accessDB as ac
import pandas as pd

db_path = 'db_v5.csv'
allergy_img_path = 'allergy_image'
ingredient_img_path = 'ingredient_image'
food_img_path = 'food_image'
df = ac.read_db(db_path)

def home_page():
    logo_text = " "
    logo_html = f"""
    <div style="position: absolute; top: -50px; right: -100px;">
        <h1 style="font-size: 24px;">{logo_text}</h1>
    </div>
    """
    st.markdown(logo_html, unsafe_allow_html=True)
    image = Image.open('logowbg.png')
    st.title('YUMSCAN')
    st.header('K-FOOD : From Seoul to your soul.')

    st.markdown("<style>h1{margin-bottom: 10px;}</style>", unsafe_allow_html=True)


    if "photo" not in st.session_state:
        st.session_state["photo"] = "not done"

    col1, col2 = st.columns([5, 3])

    def change_photo_state():
        st.session_state["photo"] = "done"

    uploaded_photo = col1.file_uploader("Upload a photo", on_change=change_photo_state)
    camera_photo = col1.camera_input("Take a photo", on_change=change_photo_state)

    if st.session_state["photo"] == "done":
        progress_bar = col1.progress(0)

        for perc_completed in range(100):
            time.sleep(0.05)
            progress_bar.progress(perc_completed + 1)

        col1.success("Photo uploaded successfully!")

    if st.session_state["photo"] == "done" and col1.button("Submit"):
        with st.expander("Preview"):
            st.write("Please double-check that you have submitted all desired photo")

            if uploaded_photo is None:
                st.image(camera_photo)
            else:
                st.image(uploaded_photo)

    col2.markdown("""
        <div style="border: 1px solid black; padding: 10px;">
            <h2>Instructions</h2>
            <p>Welcome to K-FOOD's YUMSCAN!</p>
            <p>1. Use the dropdown to select your preferred language.</p>
            <p>2. You can either upload a photo by clicking 'Upload a photo' or take a photo using the 'Take a photo' button.</p>
            <p>3. Click the 'Submit' button after uploading or taking a photo to view the preview.</p>
            <p>4. Double-check your photo in the preview section before submitting.</p>
            <p>5. Enjoy the app and discover the delicious world of K-FOOD!</p>
        </div>
    """, unsafe_allow_html=True)

def food_info_page(foods, df=df, img_path = food_img_path):
    st.title("Choose the food you want to get information")
    selected_food = st.radio("Select a food item", foods)

    if st.button("Submit"):
        for item in foods: 
            if selected_food == item: # 사용자가 고른 메뉴랑 지금 참조중인 메뉴명이 같으면
                st.write("About {}".format(item)) # 참조중인 메뉴명 출력
                st.dataframe(
                    pd.DataFrame({'Language' : ['Korean', 'English', '汉语', '台湾'],
                                  'Translate' : [df.loc[(df['ko']==item)]['ko'].values[0],
                                                df.loc[(df['ko']==item)]['en'].values[0],
                                                df.loc[(df['ko']==item)]['zh_CN'].values[0],
                                                df.loc[(df['ko']==item)]['zh_TW'].values[0]]}).set_index('Language'))
                st.image(r'{0}/{1}_image.jpg'.format(img_path, str(item))) # 참조중인 메뉴 사진 출력
                break
        

def Ingredients(selected_food):
# 음식에 들어있는 재료에 대한 사진과 설명 
    st.title("Ingredients")
    st.markdown("<p style='font-size: 20px;'>The ingredients in this food are as follows.</p>", unsafe_allow_html=True)
    st.write(" ")
    img_path = ingredient_img_path
    # ac.save_image(selected_food, df, 'ingredients.ko', img_path)

    # # 첫 번째 재료 정보 (이미지와 설명)

    
    # with cols[0]:
    #     st.image("vegetable.png", use_column_width=True)
    #     st.write("첫 번째 재료 설명")
    
    # # 두 번째 재료 정보 (이미지와 설명)
    # with cols[1]:
    #     st.image("vegetable.png", use_column_width=True)
    #     st.write("두 번째 재료 설명")

    # # 세 번째 재료 정보 (이미지와 설명)
    # with cols[2]:
    #     st.image("vegetable.png", use_column_width=True)
    #     st.write("세 번째 재료 설명")


def allergen_page(selected_food, selected_language):
    st.title("Allergen Information")
    st.markdown("<p style='font-size: 20px;'>This food can cause the following allergies.</p>", unsafe_allow_html=True)
    st.write(" ")
    st.write(" ")

    info = '알러지ko' #en 지원 안됨

    
    # 알러지에 대한 사진과 설명
    allergy_data = ac.db_finder(selected_food, info, df)

    cols = st.columns(len(allergy_data['description']))

    for i in range(len(allergy_data['description'])):
        with cols[i]:
            st.image(allergy_data['image'][i], width=200)
            st.write(allergy_data["description"][i])

def spiciness_page(selected_food):
    st.title("Spiciness Level")

    # info = '맵기단계'
    # ac.db_finder(selected_food, info, df)

    # # null 값을 선택한 경우
    # if selected_food == "치즈":
    #     is_null = st.write("UNKNOWN")
    #     if is_null:
    #         spicy_level = None
    #     else:
    #     # "치즈"인 경우 슬라이더바를 비활성화하고 불투명하게 표시
    #         with st.empty():
    #             spicy_level = None
    # else:
    #     spicy_level = st.slider("맵기 단계", 
    #                             min_value=0, max_value=3, 
    #                             value=spiciness_levels[selected_food], 
    #                             step=1, format="🌶️ %d")

    # # 선택된 맵기 단계와 null 여부에 따라 결과 출력
    # if spicy_level is None:
    #     st.write(f"{selected_food}의 맵기 단계: Null")
    # else:
    #     st.write(f"{selected_food}의 맵기 단계:", spicy_level)


def exchange_rate_page():
    def get_exchange_rates(api_key):
        url = f"https://api.currencyfreaks.com/latest?apikey=21a31a1e5b4346b3877828cea5953658"
        headers = {
            "apikey": api_key
        }
        response = requests.get(url, headers=headers)
        data = response.json()
        return data["rates"]

    base_currency = "USD"  # 기준 화폐
    target_currencies = ["USD", "JPY", "CNY", "TWD"]  # 대상 화폐들
    api_key = "21a31a1e5b4346b3877828cea5953658"  # currencyfreaks에서 발급받은 API 키를 입력

    exchange_rates = get_exchange_rates(api_key)

    # 환율 정보를 확인
    print(exchange_rates)

    krw_exchange_rate = exchange_rates.get("KRW")
    jpy_exchange_rate = exchange_rates.get("JPY")
    cny_exchange_rate = exchange_rates.get("CNY")
    twd_exchange_rate = exchange_rates.get("TWD")

    exchange = {
        "KRW": krw_exchange_rate,  
        "JPY": jpy_exchange_rate,   
        "CNY": cny_exchange_rate,   
        "TWD": twd_exchange_rate    
    }

    # 가로선 추가
    #st.markdown("<hr>", unsafe_allow_html=True)

    st.header("Today's Exchange Rate")

    BASE_currency = "KRW"
    krw_exchange_rate = float(krw_exchange_rate)
    jpy_exchange_rate = float(jpy_exchange_rate)
    cny_exchange_rate = float(cny_exchange_rate)
    twd_exchange_rate = float(twd_exchange_rate)

    usd_exchange_rate = exchange_rates.get("USD")
    usd_exchange_rate = float(usd_exchange_rate)
    USD_currency = usd_exchange_rate/krw_exchange_rate

    if USD_currency is not None:
        USD_currency = float(USD_currency)
        # 문자열을 실수형으로 변환
        st.write(f"1000 {BASE_currency} = :blue[{USD_currency*1000:.4f} USD]")
    else:
        st.write("USD의 환율 정보가 없습니다.")

    JPY_currency = jpy_exchange_rate/krw_exchange_rate

    if JPY_currency is not None:
        JPY_currency = float(JPY_currency)
        # 문자열을 실수형으로 변환
        st.write(f"1000 {BASE_currency} = :blue[{JPY_currency*1000:.4f} JPY]")
    else:
        st.write("JPY의 환율 정보가 없습니다.")

    CNY_currency = cny_exchange_rate/krw_exchange_rate

    if CNY_currency is not None:
        CNY_currency = float(CNY_currency)
        # 문자열을 실수형으로 변환
        st.write(f"1000 {BASE_currency} = :blue[{CNY_currency*1000:.4f} CNY]")
    else:
        st.write("CNY의 환율 정보가 없습니다.")

    TWD_currency = twd_exchange_rate/krw_exchange_rate

    if TWD_currency is not None:
        TWD_currency = float(TWD_currency)
        # 문자열을 실수형으로 변환
        st.write(f"1000 {BASE_currency} = :blue[{TWD_currency*1000:.4f} TWD]")
    else:
        st.write("TWD의 환율 정보가 없습니다.")

    # 가로선 추가
    st.markdown("<hr>", unsafe_allow_html=True)

    st.title("Currency Converter")
    st.write("From:", BASE_currency)

    EXCHANGE = {
        "USD": USD_currency,  
        "JPY": JPY_currency,   
        "CNY": CNY_currency,   
        "TWD": TWD_currency   
    }

    BASE_currency = "KRW"
    target_currencies = ["USD", "JPY", "CNY", "TWD"]

    BASE = st.number_input("AMOUNT", key="BASE", min_value=0.01)

    #st.write("choose target_currencies:")
    TARGET = st.selectbox("TO", target_currencies, key="TARGET")

    converted_amount = BASE * EXCHANGE[TARGET]
    st.title(f"{BASE:.2f} {BASE_currency} = :blue[{converted_amount:.2f} {TARGET}]")

# Main app
def main():
    st.set_page_config(page_title="YumScan", page_icon=":pizza:", layout="wide")
    
    # Create a sidebar navigation menu
    image = Image.open('logowbg.png')

    st.sidebar.image("logowbg.png", use_column_width=True)
    navigation = st.sidebar.radio("YUMSCAN", ["🏠 Home", "🍔 Food Information", "🥗 Ingredients", "🚫 Allergen Information", "🌶️ Spiciness Level", "💱 Currency Converter"], key="navigation")
    
    # Separator line
    st.sidebar.markdown("<div class='sidebar-separator'></div>", unsafe_allow_html=True)

    # Language selection using selectbox
    selected_language = st.sidebar.selectbox("Select Language", ["English", "Chinese", "Japanese"])

    # 음식 목록 생성
    foods = ['치즈퐁듀랍스터&씨푸드', '스모크우드박스안심스테이크'] # 은지네에서 받은 ocr 결과 리스트로 수정

 
    # 음식 선택
    selected_food = st.selectbox("음식 선택", foods)
    
    
    if navigation == "🏠 Home":
        home_page()
    elif navigation == "🍔 Food Information":
        ac.save_image(foods, 'ko',df=df, img_path=food_img_path)
        food_info_page(foods)
    elif navigation == "🥗 Ingredients":
        Ingredients(selected_food)
    elif navigation == "🚫 Allergen Information":
        allergen_page(selected_food, selected_language)
    elif navigation == "🌶️ Spiciness Level":
        spiciness_page(selected_food)
    elif navigation == "💱 Currency Converter":
        exchange_rate_page()

if __name__ == "__main__":
    main()

# Made with Streamlit, MainMenu 제거
st.markdown('''
    <style>
        #MainMenu {
            visibility: hidden;
        }
        
        footer {
            visibility: hidden;
        }    
    </style>
    ''', unsafe_allow_html=True)  
