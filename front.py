"""
Фронт на streamlit
"""

import streamlit as st
import pandas as pd
import requests

from enviroment import API_URL as ENVIROMENT_API_URL


st.set_page_config(
    page_title="Управление данными",
    layout="wide"
)

API_URL = ENVIROMENT_API_URL

st.title("Вебморда")

tab1, tab2 = st.tabs(["Получение данных", "Загрузка данных"])

with tab1:
    st.header("Получение данных из базы")

    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        if st.button("Получить данные", type="primary", use_container_width=True):
            try:
                response = requests.get(f"{API_URL}/data")
                if response.status_code == 200:
                    data = response.json()
                    if data.get("data"):
                        df = pd.DataFrame(data["data"])
                        st.session_state['data_df'] = df
                        st.session_state['data_loaded'] = True
                    else:
                        st.info("Нет данных для отображения")
                        st.session_state['data_loaded'] = False
                else:
                    st.error(f"Ошибка при получении данных: {response.status_code}")
            except requests.exceptions.ConnectionError:
                st.error("Не удалось подключиться к API. Убедитесь, что сервер запущен.")
            except Exception as e:
                st.error(f"Произошла ошибка: {str(e)}")

    if st.session_state.get('data_loaded', False):
        df = st.session_state['data_df']

        st.subheader("Данные в таблице")

        column_config = {
            "db_id": "ID",
            "rate_id": "Rate ID",
            "rate_name": "Название тарифа",
            "service_id": "Service ID",
            "service_name": "Название услуги",
            "price": st.column_config.NumberColumn(
                "Цена",
                format="%d ₽",
                help="Цена в рублях"
            )
        }

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config=column_config
        )

with tab2:
    st.header("Загрузка новых данных")

    upload_method = st.radio(
        "Выберите метод загрузки:",
        ["Ввод вручную", "Загрузка из файла"],
        horizontal=True
    )

    if upload_method == "Ввод вручную":
        st.subheader("Введите данные вручную")

        with st.form("manual_input_form"):
            col1, col2 = st.columns(2)

            with col1:
                db_id = st.number_input("db_id", min_value=1, step=1, value=1)
                rate_id = st.number_input("rate_id", min_value=1, step=1, value=101)
                rate_name = st.text_input("rate_name", value="Базовый")

            with col2:
                service_id = st.number_input("service_id", min_value=1, step=1, value=201)
                service_name = st.text_input("service_name", value="Интернет")
                price = st.number_input("price", min_value=1, step=1, value=500)

            submitted = st.form_submit_button("Сохранить", use_container_width=True)

            if submitted:
                data = {
                    "db_id": db_id,
                    "rate_id": rate_id,
                    "rate_name": rate_name,
                    "service_id": service_id,
                    "service_name": service_name,
                    "price": price
                }
                try:
                    response = requests.post(f"{API_URL}/data", json=data)

                    if response.status_code == 200:
                        result = response.json()
                        if "успешно" in result.get("message", "").lower():
                            st.success("Данные успешно сохранены!")
                        else:
                            st.warning(result.get("message", "Неизвестный ответ"))
                    else:
                        st.error(f"Ошибка при сохранении: {response.status_code}")
                except requests.exceptions.ConnectionError:
                    st.error("Не удалось подключиться к API")
                except Exception as e:
                    st.error(f"Ошибка: {str(e)}")

    else:
        st.subheader("Загрузка данных из файла")

        uploaded_file = st.file_uploader(
            "Выберите файл",
            type=['csv', 'xlsx', 'xls'],
            help="Загрузите файл с данными"
        )

        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)

                required_columns = ['db_id', 'rate_id', 'rate_name', 'service_id', 'service_name', 'price']

                if all(col in df.columns for col in required_columns):
                    st.success(f"Файл успешно загружен! Найдено {len(df)} записей")

                    st.subheader("Предпросмотр данных")
                    st.dataframe(df.head(10), use_container_width=True)

                    col1, col2 = st.columns(2)
                    with col1:
                        st.info(f"Всего записей: {len(df)}")
                    with col2:
                        st.info(f"Дубликатов по db_id: {df.duplicated('db_id').sum()}")

                    if st.button("Загрузить все данные", type="primary", use_container_width=True):
                        status_text = st.empty()

                        success_count = 0
                        error_count = 0

                        for index, row in df.iterrows():
                            try:
                                data = {
                                    "db_id": int(row['db_id']),
                                    "rate_id": int(row['rate_id']),
                                    "rate_name": str(row['rate_name']),
                                    "service_id": int(row['service_id']),
                                    "service_name": str(row['service_name']),
                                    "price": int(row['price'])
                                }

                                response = requests.post(f"{API_URL}/data", json=data)

                                if response.status_code == 200:
                                    success_count += 1
                                else:
                                    error_count += 1

                            except Exception as e:
                                error_count += 1
                                st.error(f"Ошибка в строке {index + 1}: {str(e)}")

                        status_text.empty()

                        if error_count == 0:
                            st.success(f"Все {success_count} записей успешно загружены!")
                        else:
                            st.warning(f"Загрузка завершена. Успешно: {success_count}, Неуспешно: {error_count}")

                else:
                    missing = set(required_columns) - set(df.columns)
                    st.error(f"В файле отсутствуют колонки: {missing}")

            except Exception as e:
                st.error(f"Ошибка при чтении файла: {str(e)}")
