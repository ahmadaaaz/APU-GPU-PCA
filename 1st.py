import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="APU-GPU Optimizasyon", layout="wide")

AIRCRAFT_DATABASE = {
    "Orta Gövde (A320/ B747)": {"burn_rate": 120, "gpu_req": 90}, #kg/saat, #kW
    "Geniş Gövde (A350/ B777)": {"burn_rate": 300, "gpu_req": 180},
    "Küçük Gövde": {"burn_rate": 60, "gpu_req": 45},
}

CO2_FACTOR = 3.16
FUEL_PRICE_KG = 0.68 #USD
ELEC_PRICE_KWH = 0.11 #USD/


st.title("Uçak Yerde Emisyon Azaltımı için APU–GPU/PCA Optimizasyon Platformu")
st.markdown("---")

st.header("Operasyonel Parametreler")
selected_model = st.selectbox("Uçak Tipi Seçiniz", list(AIRCRAFT_DATABASE.keys()))
taxi_in_out = st.number_input("Havaalanın Taxi-in/out süresi ne kadar?", min_value=0)
turnaround_time = st.slider("Toplam Turnaround Süresi (Dakika)", 10+taxi_in_out,80)
optimized_apu_usage = st.number_input(f"Önerilen Senaryo APU Süresi (Dakika)", min_value=10, max_value=turnaround_time)

specs = AIRCRAFT_DATABASE[selected_model]
gpu_time = turnaround_time - optimized_apu_usage
st.info(f"GPU çalışma süresi {gpu_time} dakikadir.")

#==================================================================================================

ref_fuel = turnaround_time * specs["burn_rate"]
ref_co2 = ref_fuel * CO2_FACTOR
ref_cost = ref_fuel * FUEL_PRICE_KG
st.markdown("---")

st.write('''### Referans Senaryo:''')
m1, m2, m3 = st.columns(3)
m1.metric("Harcanan yakıt", f"{ref_fuel:.1f} kg")#, delta=f"-{((saved_fuel/ref_fuel)*100):.1f}%")
m2.metric("CO₂ Emisyonu", f"{ref_co2:.1f} kg")#, delta="-75%" if saved_co2 > 0 else "0%")
m3.metric("Toplam Sarfiyat", f"${ref_cost:.2f}")#, delta=f"${ref_cost:.2f} Base", delta_color="inverse")

opt_fuel = optimized_apu_usage * specs["burn_rate"]
opt_co2 = opt_fuel * CO2_FACTOR
opt_elec_cost = (gpu_time / 60) * specs["gpu_req"] * ELEC_PRICE_KWH
opt_total_cost = (opt_fuel * FUEL_PRICE_KG) + opt_elec_cost

saved_fuel = ref_fuel - opt_fuel
saved_co2 = ref_co2 - opt_co2
saved_money = ref_cost - opt_total_cost

st.write('''### Önerilen Senaryo:''')
m1, m2, m3 = st.columns(3)
m1.metric("Harcanan yakıt", f"{ref_fuel-saved_fuel:.1f} kg", delta=f"-{((saved_fuel/ref_fuel)*100):.1f}%", delta_color="blue")
m2.metric("CO₂ Emisyonu", f"{ref_co2-saved_co2:.1f} kg", delta="-75%" if saved_co2 > 0 else "0%", delta_color="blue")
m3.metric("Toplam Maliyet", f"${ref_cost-saved_money:.2f}", delta=f"${saved_money:.2f} Base")

st.markdown("### Senaryo Analizi ve Karşılaştırma")
col_chart1, col_chart2 = st.columns(2)

chart_data = pd.DataFrame({
    "Senaryo": ["Referans (APU)", "Önerilen (GPU/PCA)"],
    "Emisyon (kg CO2)": [ref_co2, opt_co2],
    "Maliyet ($)": [ref_cost, opt_total_cost]
})

with col_chart1:
    fig1, ax1 = plt.subplots()
    ax1.bar(chart_data["Senaryo"], chart_data["Emisyon (kg CO2)"], color=["#e74c3c", "#2ecc71"])
    ax1.set_ylabel("CO2 Salınımı (kg)")
    st.pyplot(fig1)

with col_chart2:
    fig2, ax2 = plt.subplots()
    ax2.bar(chart_data["Senaryo"], chart_data["Maliyet ($)"], color=["#c0392b", "#2980b9"])
    ax2.set_ylabel("Operasyonel Maliyet ($)")
    st.pyplot(fig2)

if saved_money > 0:
    st.success(f"Optimizasyon Başarılı: Bu operasyonda toplam ${saved_money:.2f} tasarruf ve {saved_co2:.1f} kg karbon engelleme saptanmıştır.")
