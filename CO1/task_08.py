
START
    total = 0
    payments = empty list

    FOR each farmer
        INPUT litres, fat, snf

        fat_steps = ROUND((fat - 3.5) / 0.1)
        snf_steps = ROUND((snf - 8.5) / 0.1)

        rate = 30 + fat_steps * 0.40 + snf_steps * 0.30
        payment = ROUND(litres * rate, 2)

        ADD payment TO payments
        total = total + payment

        DISPLAY rate, payment
    END FOR

    DISPLAY total
STOP
