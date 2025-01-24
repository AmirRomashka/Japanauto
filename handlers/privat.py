

from icecream import ic

from aiogram.utils.formatting import as_list, as_marked_section, Bold
from aiogram import types, Router, F

from aiogram.filters import CommandStart, Command, or_f, StateFilter


from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext


from kbdb.keyboard import get_keyboard
from request.calcul import CalCulAPI
from request.currence import CBRF

user_private = Router()




@user_private.message(CommandStart())
@user_private.message(F.text.lower() == "калькулятор")
async def start(message : types.Message, state : FSMContext):
    await state.clear()
    await message.answer(
        f"Здравствуйте {message.from_user.first_name} !\nВы в калькуляторе для подсчета ориентировочной стоимости\nВыберите страну в которой хотите купить авто: ",
        reply_markup = get_keyboard(
            "Япония",
            "Китай",
            "Корея",
            sizes = (1,1,1)
            
        )
    
    )

#FSM.calculator
class CostCalculation(StatesGroup):
    engine = State()
    power_unit = State()
    power = State()
    value = State()
    age = State()
    price = State()
    
    text = {
        "CostCalculation:engine":"Выберите тип двигателя заново",
        "CostCalculation:value":"Введите объем двигателя заново",
        "CostCalculation:power_unit":"Выберите тип величины заново",
        "CostCalculation:power":"Введите мощность автомобиля заново",
        "CostCalculation:age":"Выберите возраст авто заново",
        "CostCalculation:price":"Введите цену машины заново"
    }
    keyboard = {
        "CostCalculation:engine" : get_keyboard("Бензиновый", "Дизельный", "Гибрид", "Электрический","Отмена","Назад", sizes = (1,1,1,1,2)),
        "CostCalculation:value" : get_keyboard("Отмена","Назад", sizes = (1,1,2)),
        "CostCalculation:power_unit" : get_keyboard("Л.С.","кВт","Отмена","Назад", sizes = (1,1,2)),
        "CostCalculation:power" : get_keyboard("Отмена","Назад", sizes = (1,1,2)),
        "CostCalculation:age" : get_keyboard("0-3", "3-5", "5-7", "7-0","Отмена","Назад", sizes = (2,2,2)), 
    }

#start JPY
@user_private.message(StateFilter(None), F.text.lower() == "япония")
async def type_engine(message : types.Message, state : FSMContext):
    await state.update_data(country = "JPY")
    await message.answer("Выберите тип двигателя:", reply_markup = get_keyboard("Бензиновый", "Дизельный", "Гибрид", "Электрический","Отмена","Назад",sizes = (1,1,1,1,2)))
    await state.set_state(CostCalculation.engine) 
#start CNY
@user_private.message(StateFilter(None), F.text.lower() == "китай")
async def type_engine(message : types.Message, state : FSMContext):
    await state.update_data(country = "CNY")
    await message.answer("Выберите тип двигателя:", reply_markup = get_keyboard("Бензиновый", "Дизельный", "Гибрид", "Электрический","Отмена","Назад",sizes = (1,1,1,1,2)))
    await state.set_state(CostCalculation.engine) 
#start KRW
@user_private.message(StateFilter(None), F.text.lower() == "корея")
async def type_engine(message : types.Message, state : FSMContext):
    await state.update_data(country = "KRW")
    await message.answer("Выберите тип двигателя:", reply_markup = get_keyboard("Бензиновый", "Дизельный", "Гибрид", "Электрический","Отмена","Назад",sizes = (1,1,1,1,2)))
    await state.set_state(CostCalculation.engine) 


#Отмена и назад
@user_private.message(StateFilter("*"), F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return # Если состояние отсутсствует то используется данный if и возвращает None после - ничего не происходит
    await state.clear() # удаляет состояние user
    await message.answer("Действия отменены", reply_markup=get_keyboard("Калькулятор"))

@user_private.message(F.text.casefold() == "назад")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state == "CostCalculation:engine":
        await message.answer(text = "Предидущего шага нет")
        return
    
    previous = None
    for step in CostCalculation.__all_states__:
        ic(step)
        if step == current_state:
            await state.set_state(previous)
            await message.answer(f"Вы вернулись на предидущий шаг:\n{CostCalculation.text[previous.state]} ", reply_markup = CostCalculation.keyboard[previous.state])
            return
        previous = step
#engine and power_unit

@user_private.message(CostCalculation.engine, F.text == "Бензиновый")
async def input_value(message : types.Message, state : FSMContext):
    await state.update_data(engine = 1)
    await state.update_data(power_unit = 1)
    await message.answer("Укажите объем двигателя в см³:", reply_markup = get_keyboard("Отмена","Назад", ))
    await state.set_state(CostCalculation.value)

@user_private.message(CostCalculation.engine, F.text == "Дизельный")
async def input_value(message : types.Message, state : FSMContext):
    await state.update_data(engine = 2)
    await state.update_data(power_unit = 1)
    await message.answer("Укажите объем двигателя в см³:", reply_markup = get_keyboard("Отмена","Назад", ))
    await state.set_state(CostCalculation.value)



#input power_unir
@user_private.message(CostCalculation.engine, F.text == "Гибрид")
async def choice_power(message : types.Message, state : FSMContext):  
    await state.update_data(engine = 3)
    await state.update_data(power_unit = 1)
    await message.answer("Укажите объем двигателя в см³:", reply_markup = get_keyboard("Отмена","Назад", ))
    await state.set_state(CostCalculation.value)

@user_private.message(CostCalculation.engine, F.text == "Электрический")
async def choice_power(message : types.Message, state : FSMContext):  
    await state.update_data(engine = 4)
    await state.update_data(value = "1")
    await message.answer("Выберите величину измерения мощности:", reply_markup = get_keyboard("Л.С.","кВт","Отмена","Назад", sizes = (1,1,2)))
    await state.set_state(CostCalculation.power_unit)

#power_unit

@user_private.message(CostCalculation.power_unit, F.text == "Л.С.")
async def input_power(message : types.Message, state : FSMContext):
    await state.update_data(power_unit = 1)
    await message.answer("Укажите мощность двигателя:", reply_markup = get_keyboard("Отмена","Назад", ))
    await state.set_state(CostCalculation.power)

@user_private.message(CostCalculation.power_unit, F.text == "кВт")
async def input_power(message : types.Message, state : FSMContext):
    await state.update_data(power_unit = 2)
    await message.answer("Укажите мощность двигателя:", reply_markup = get_keyboard("Отмена","Назад",))
    await state.set_state(CostCalculation.power)







#value
@user_private.message(CostCalculation.value, F.text.isnumeric())
async def input_power(message : types.Message, state : FSMContext):  
    await state.update_data(value = message.text)
    await message.answer("Укажите мощность двигателя:", reply_markup = get_keyboard("Отмена","Назад",))
    await state.set_state(CostCalculation.power)




#power
@user_private.message(CostCalculation.power, F.text.isnumeric())
async def input_age(message : types.Message, state : FSMContext):
    await state.update_data(power = message.text)
    
    await message.answer("Укажите возраст автомобиля:", reply_markup = get_keyboard("0-3","3-5","5-7","7-0","Отмена","Назад", sizes = (2,2,2,)))
    await state.set_state(CostCalculation.age)

#input age
@user_private.message(CostCalculation.age, F.text)
async def input_price(message : types.Message, state : FSMContext):
    await state.update_data(age = message.text)
    country2 = await state.get_data()
    ic(country2)
    if country2["country"] == "JPY":
        ic("Япония")
        await message.answer("Укажите цену автомобиля на аукционе (в йенах): (Введите число)", reply_markup = get_keyboard("Отмена","Назад",))
        await state.set_state(CostCalculation.price)
    elif country2["country"] == "KRW":
        ic("Китай")
        await message.answer("Укажите цену автомобиля на аукционе (в вонах): (Введите число)", reply_markup = get_keyboard("Отмена","Назад",))
        await state.set_state(CostCalculation.price)
    elif country2["country"] == "CNY":
        ic("Корея")
        await message.answer("Укажите цену автомобиля на аукционе (в юанях): (Введите число)", reply_markup = get_keyboard("Отмена","Назад",))
        await state.set_state(CostCalculation.price)
    del country
    
#calculate price
@user_private.message(CostCalculation.price, F.text.isnumeric())
async def calculate_price(message : types.Message, state : FSMContext):
    await state.update_data(price = message.text)
    data = await state.get_data()
    await state.clear()
    
    ic("Старт")
    if data["country"] == "JPY":
        object_CalCul = CalCulAPI()
        total = await object_CalCul.search_price(info = data)
        ic(total)
        object_CBRF = CBRF()
        value_100_yen = await object_CBRF.value_yen()
        ic(data)
        data["price"] = int(data["price"]) * (int(value_100_yen) / 100)
        yen2 = 0
        yen_of_auto = 0
        if int(data["price"]) >= 1000000 and int(data["price"]) < 1500000:
            yen_of_auto = 20000
        elif int(data["price"]) >= 1500000 and int(data["price"]) < 2000000:
            yen_of_auto = 30000
        elif int(data["price"]) >= 2000000 and int(data["price"]) < 2500000:
            yen_of_auto = 50000
        elif int(data["price"]) >= 2500000 and int(data["price"]) < 3000000:
            yen_of_auto = 60000
        elif int(data["price"]) >= 3000000 and int(data["price"]) < 3500000:
            yen_of_auto = 70000
        elif int(data["price"]) >= 3500000 and int(data["price"]) < 4000000:
            yen_of_auto = 85000
        elif int(data["price"]) >= 4000000 and int(data["price"]) < 4500000:
            yen_of_auto = 100000
        elif int(data["price"]) >= 4500000 and int(data["price"]) < 5000000:
            yen_of_auto = 115000
        elif int(data["price"]) >= 5000000:
            yen_of_auto = 130000
        if data["engine"] == 3:
            yen2 += 400000
        elif data["engine"] == 4:
            yen2 += 450000
        ic(total,value_100_yen, yen2, yen_of_auto, data)


        if data["engine"] in [1, 2]:
            price_auto = int(total["total2"]) + 90000 + ((int(yen_of_auto) + 125000) * value_100_yen / 100)
            yen_of_auto = int(yen_of_auto) + 125000
            ic(price_auto)
            cost_message = (
                f"Стоимость автомобиля: {int(data['price'])} ₽\n"
                f"--------------------\n"
                f"Сборы:\n"
                f"--------------------\n"
                f"\tТаможенный сбор:         {total['sbor']} ₽\n"
                f"\tТаможенная пошлина:     {total['tax']} ₽\n"
                f"\tУтилизационный сбор:    {total['util']} ₽\n"
                f"--------------------\n"
                f"Услуги:\n"
                f"--------------------\n"
                f"\tРасходы по Японии:    {yen_of_auto}¥\n"
                f"\tБрокер, СВХ, СБКТС:    50 000 ₽\n"
                f"\tКомиссия:    40 000 ₽\n"
                f"--------------------\n"
                f"\t\tИтоговая стоимость    {int(price_auto)} ₽"
            )
            await message.answer(cost_message, reply_markup=get_keyboard("Калькулятор"))


        else:
            try:
                price_auto = int(total["total2"]) + 90000 + ((int(yen2) + int(yen_of_auto) + 125000) * value_100_yen / 100)
                ic(price_auto)
                yen_of_auto = int(yen_of_auto) + int(yen2) + 125000
                if data["engine"] != 4:
                    cost_message = (
                        f"Стоимость автомобиля: {int(data['price'])} ₽\n"
                        f"--------------------\n"
                        f"Сборы:\n"
                        f"--------------------\n"
                        f"\tТаможенный сбор:         {total['sbor']} ₽\n"
                        f"\tТаможенная пошлина:     {total['tax']} ₽\n"
                        f"\tУтилизационный сбор:    {total['util']} ₽\n"
                        f"--------------------\n"
                        f"Услуги:\n"
                        f"--------------------\n"
                        f"\tРасходы по Японии:    {yen_of_auto}¥\n"
                        f"\tБрокер, СВХ, СБКТС:    50 000 ₽\n"
                        f"\tКомиссия:    40 000 ₽\n"
                        f"--------------------\n"
                        f"\t\tИтоговая стоимость    {int(price_auto)} ₽"
                    )
                    await message.answer(cost_message, reply_markup=get_keyboard("Калькулятор"))
                else:
                    cost_message = (
                        f"Стоимость автомобиля: {int(data['price'])} ₽\n"
                        f"--------------------\n"
                        f"Сборы:\n"
                        f"--------------------\n"
                        f"\tТаможенный сбор:         {total['sbor']} ₽\n"
                        f"\tТаможенная пошлина:     {total['tax']} ₽\n"
                        f"\tУтилизационный сбор:    {total['util']} ₽\n"
                        f"\tАкциз:    {total["excise"]} ₽\n"
                        f"\tНДС (20%)    {total["nds"]} ₽\n"
                        f"--------------------\n"
                        f"Услуги:\n"
                        f"--------------------\n"
                        f"\tРасходы по Японии:    {yen_of_auto}¥\n"
                        f"\tБрокер, СВХ, СБКТС:    50 000 ₽\n"
                        f"\tКомиссия:    40 000 ₽\n"
                        f"--------------------\n"
                        f"\t\tИтоговая стоимость    {int(price_auto)} ₽"
                    )
                    await message.answer(cost_message, reply_markup=get_keyboard("Калькулятор"))

            except (KeyError, ValueError, TypeError) as e:
                print(f"Ошибка при формировании сообщения о стоимости: {e}")
                await message.answer("Произошла ошибка при расчете стоимости. Попробуйте позже.")
    elif data["country"] == "KRW":
        object_CalCul = CalCulAPI()
        total = await object_CalCul.search_price(info = data)
        ic(total)
        object_CBRF = CBRF()
        value_1000_von = await object_CBRF.value_von()
        ic(data)
        data["price"] = int(data["price"]) * (int(value_1000_von) / 1000)
        price_auto = int(total["total2"]) + 115000 + (1700000 * (value_1000_von / 1000))
        if data["engine"] != 4:
            cost_message = (
                    f"Стоимость автомобиля: {int(data['price'])} ₽\n"
                    f"--------------------\n"
                    f"Сборы:\n"
                    f"--------------------\n"
                    f"\tТаможенный сбор:         {total['sbor']} ₽\n"
                    f"\tТаможенная пошлина:     {total['tax']} ₽\n"
                    f"\tУтилизационный сбор:    {total['util']} ₽\n"
                    f"--------------------\n"
                    f"Услуги:\n"
                    f"--------------------\n"
                    f"\tРасходы по Корее:    1 700 000 ₩\n"
                    f"\tБрокер, СВХ, СБКТС:    75 000 ₽\n"
                    f"\tКомиссия:    40 000 ₽\n"
                    f"--------------------\n"
                    f"\t\tИтоговая стоимость    {int(price_auto)} ₽"
                )
            await message.answer(cost_message, reply_markup=get_keyboard("Калькулятор"))
        else:
            cost_message = (
                    f"Стоимость автомобиля: {int(data['price'])} ₽\n"
                    f"--------------------\n"
                    f"Сборы:\n"
                    f"--------------------\n"
                    f"\tТаможенный сбор:         {total['sbor']} ₽\n"
                    f"\tТаможенная пошлина:     {total['tax']} ₽\n"
                    f"\tУтилизационный сбор:    {total['util']} ₽\n"
                    f"\tАкциз:    {total["excise"]} ₽\n"
                    f"\tНДС (20%)    {total["nds"]} ₽\n"
                    f"--------------------\n"
                    f"Услуги:\n"
                    f"--------------------\n"
                    f"\tРасходы по Корее:    1 700 000 ₩\n"
                    f"\tБрокер, СВХ, СБКТС:    75 000 ₽\n"
                    f"\tКомиссия:    40 000 ₽\n"
                    f"--------------------\n"
                    f"\t\tИтоговая стоимость    {int(price_auto)} ₽"
                )
            await message.answer(cost_message, reply_markup=get_keyboard("Калькулятор"))

    elif data["country"] == "CNY":
        object_CalCul = CalCulAPI()
        total = await object_CalCul.search_price(info = data)
        ic(total)
        object_CBRF = CBRF()
        value_uan = await object_CBRF.value_uan()
        ic(data)
        data["price"] = int(data["price"]) * value_uan
        price_auto = total["total2"] + 115000 + (15000 * value_uan)
        ic(price_auto, data["price"], value_uan, total)
        if data["engine"] != 4:
            cost_message = (
                    f"Стоимость автомобиля: {int(data['price'])} ₽\n"
                    f"--------------------\n"
                    f"Сборы:\n"
                    f"--------------------\n"
                    f"\tТаможенный сбор:         {total['sbor']} ₽\n"
                    f"\tТаможенная пошлина:     {total['tax']} ₽\n"
                    f"\tУтилизационный сбор:    {total['util']} ₽\n"
                    f"--------------------\n"
                    f"Услуги:\n"
                    f"--------------------\n"
                    f"\tРасходы по Китаю:    15000 元\n"
                    f"\tБрокер, СВХ, СБКТС:    75 000 ₽\n"
                    f"\tКомиссия:    40 000 ₽\n"
                    f"--------------------\n"
                    f"\t\tИтоговая стоимость    {int(price_auto)} ₽"
                )
            await message.answer(cost_message, reply_markup=get_keyboard("Калькулятор"))
        else:
            cost_message = (
                    f"Стоимость автомобиля: {int(data['price'])} ₽\n"
                    f"--------------------\n"
                    f"Сборы:\n"
                    f"--------------------\n"
                    f"\tТаможенный сбор:         {total['sbor']} ₽\n"
                    f"\tТаможенная пошлина:     {total['tax']} ₽\n"
                    f"\tУтилизационный сбор:    {total['util']} ₽\n"
                    f"\tАкциз:    {total["excise"]} ₽\n"
                    f"\tНДС (20%)    {total["nds"]} ₽\n"
                    f"--------------------\n"
                    f"Услуги:\n"
                    f"--------------------\n"
                    f"\tРасходы по Китаю:    15000 元\n"
                    f"\tБрокер, СВХ, СБКТС:    75 000 ₽\n"
                    f"\tКомиссия:    40 000 ₽\n"
                    f"--------------------\n"
                    f"\t\tИтоговая стоимость    {int(price_auto)} ₽"
                )
            await message.answer(cost_message, reply_markup=get_keyboard("Калькулятор"))




    del data
    
    ic("Завершенно")
    #Выход/назад___________________________________________________________________________________________________________________________________________________________


    
    

    
        
   


     