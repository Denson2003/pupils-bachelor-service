from fastapi import FastAPI
import pandas as pd
import os

app = FastAPI(title="Pupils Bachelor Service")

# Данные студентов
data = {
    "name": ["Анна", "Иван", "Ольга", "Петр", "Мария", "Сергей", "Елена"],
    "specialization": [
        "Информационная безопасность",
        "Автоматизированные системы",
        "Защищенные АС",
        "Компьютерная безопасность",
        "Защищенные АС",
        "Автоматизированные системы",
        "Информационная безопасность"
    ],
    "grade": [4, 5, 4, 3, 5, 4, 5],
    "course": [4, 4, 4, 4, 3, 4, 4]
}
df = pd.DataFrame(data)

# Сохраняем в CSV
df.to_csv("pupils.csv", index=False)

@app.get("/")
def root():
    return {
        "service": "Pupils Bachelor Service",
        "message": "Я стану бакалавром в области защищенных автоматизированных систем"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/students")
def get_students():
    return df.to_dict(orient="records")

@app.get("/bachelor")
def get_bachelor():
    # Бакалавр: оценка >= 4 и курс >= 3
    bachelor_mask = (df["grade"] >= 4) & (df["course"] >= 3)
    candidates = df[bachelor_mask]
    return {
        "message": "Я стану бакалавром в области защищенных автоматизированных систем",
        "total_candidates": len(candidates),
        "by_specialization": candidates.groupby("specialization").size().to_dict(),
        "candidates": candidates.to_dict(orient="records")
    }
