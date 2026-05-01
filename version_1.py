def phoenix_score(pao2_fio2, ventilation, vaso_count, lactate, map_low, platelets, inr, gcs):
 #0-13 баллов
    score = 0
    if ventilation and pao2_fio2 < 100:
        score += 3
    elif ventilation and pao2_fio2 <= 200:
        score += 2
    elif pao2_fio2 < 400:
        score += 1
    score += min(vaso_count, 2)
    if lactate >= 5:
        score += 1
        if lactate >= 11:
            score += 1
    if map_low:
        score += 1
    if platelets < 100:
        score += 1
    if inr > 1.3:
        score += 1
    score = min(score, 2)  # максимум 2 балла
    if gcs <= 10: #по мозгу
        score += 1
    return score
def diagnose(infection, sofa, lactate, vaso, pao2_fio2=400, vent=False, vaso_count=1,map_low=False, platelets=200, inr=1.0, gcs=15):
    print("ДИАГНОСТИКА СЕПСИСА")
    if not infection:
        print("НЕТ СЕПСИСА - нет признаков инфекции")
        return
    phoenix = phoenix_score(pao2_fio2, vent, vaso_count, lactate, map_low, platelets, inr, gcs)
    print(f"Phoenix Score: {phoenix} баллов")
    if sofa >= 2 or phoenix >= 2:
        print("СЕПСИС: ДА")

        cardio_score = min(vaso_count, 2) + (1 if lactate >= 5 else 0) + (1 if map_low else 0)
        if (vaso and lactate > 2) or cardio_score >= 1:
            print("\033[1mЕСТЬ СЕПТИЧЕСКИЙ ШОК\033[0m")
            print("\nСРОЧНЫЕ ДЕЙСТВИЯ:")
            print("вазопрессоры (норадреналин)")
            print("антибиотики широкого спектра")
            print("перевод в ОРИТ")
            print("мониторинг лактата")
        else:
            print("НЕТ СЕПТИЧЕСКОГО ШОКА")
            print("\nЛЕЧЕНИЕ:")
            print("антибиотики")
            print("мониторинг органов")
            print("мониторинг лактата")
    else:
        print("НЕТ СЕПСИСА", f"(нужно ≥2 баллов, сейчас SOFA={sofa}, Phoenix={phoenix})")
        if sofa == 1 or phoenix == 1:
            print("Повторите оценку через 4-6 часов")

print("\n\033[1mПациент с пневмонией\033[0m")
diagnose(
    infection=True,
    sofa=2,
    lactate=3.2,
    vaso=True,
    pao2_fio2=320,
    vaso_count=1
)
print("\n\033[1mОрганная дисфункция, но нет инфекции\n\033[0m")
diagnose(
    infection=False,
    sofa=2,
    lactate=2.5,
    vaso=True
)