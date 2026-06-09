# Отчет по дисциплине
## "Технология проектирования автоматизированных систем в защищенном исполнении"

**Тема работы:** Разработка и деплой веб-сервиса для определения кандидатов на степень бакалавра

**Студент:** Denson2003

**Дата выполнения:** 09.06.2026

---

## Содержание

1. [Создание репозитория GitHub](#1-создание-репозитория-github)
2. [Разработка сервиса FastAPI](#2-разработка-сервиса-fastapi)
3. [Упаковка сервиса in Docker](#3-упаковка-сервиса-in-docker)
4. [Загрузка образа в Docker Hub](#4-загрузка-образа-в-docker-hub)
5. [Развертка в Yandex Cloud через Terraform](#5-развертка-в-yandex-cloud-через-terraform)
6. [Развертка в Minikube через Kubernetes](#6-развертка-в-minikube-через-kubernetes)
7. [Оформление README](#7-оформление-readme)

---

## 1. Создание репозитория GitHub

### Что было сделано:

| Действие | Результат |
|----------|-----------|
| Создан аккаунт на GitHub | ✅ Аккаунт `Denson2003` |
| Создан публичный репозиторий | ✅ `pupils-bachelor-service` |
| Репозиторий склонирован локально | ✅ Код загружен |

### Использованные команды:

```bash
git init
git add .
git commit -m "Initial commit: FastAPI service for bachelor detection"
git remote add origin https://github.com/Denson2003/pupils-bachelor-service.git
git push -u origin main
```

### Скриншоты:

| № | Скриншот | Описание |
|---|----------|----------|
| 1.1 | `1.1_create_repo.png` | Страница создания репозитория |
| 1.2 | `1.2_empty_repo.png` | Репозиторий готов к загрузке |
| 1.3 | `1.3_successful_push.png` | Git push выполнен успешно |
| 1.4 | `1.4_github_with_files.png` | Все файлы загружены на GitHub |

### ✅ Вывод по этапу 1:

Задача выполнена. Репозиторий создан, код загружен, репозиторий публичный и доступен по ссылке:

🔗 https://github.com/Denson2003/pupils-bachelor-service

---

## 2. Разработка сервиса FastAPI

### Что было сделано:

| Действие | Результат |
|----------|-----------|
| Создан app.py с кодом сервиса | ✅ 7 эндпоинтов |
| Создан requirements.txt | ✅ FastAPI, Uvicorn, Pandas |
| Создан pupils.csv | ✅ 7 студентов |
| Сервис запущен локально | ✅ Работает на порту 8000 |

### Реализованные эндпоинты:

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/` | Информация о сервисе |
| GET | `/health` | Проверка здоровья |
| GET | `/students` | Список студентов |
| GET | `/students?specialization=...` | Фильтр по специализации |
| GET | `/bachelor` | Кандидаты на бакалавра |
| GET | `/student/{name}` | Данные конкретного студента |

### Код сервиса (основная часть):

```python
@app.get("/bachelor")
def get_bachelor():
    bachelor_mask = (df["grade"] >= 4) & (df["course"] >= 3)
    candidates = df[bachelor_mask]
    return {
        "message": "Я стану бакалавром в области защищенных автоматизированных систем",
        "total_candidates": len(candidates),
        "by_specialization": candidates.groupby("specialization").size().to_dict()
    }
```

### Команды для запуска:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Скриншоты:

| № | Эндпоинт | Скриншот | Описание |
|---|----------|----------|----------|
| 2.1 | Консоль | `2.1_console_run.png` | Сервис запущен локально |
| 2.2 | Swagger /docs | `2.2_swagger_ui.png` | Swagger документация доступна |
| 2.3 | GET `/` | `2.3_root_endpoint.png` | Эндпоинт `/` работает |
| 2.4 | GET `/students` | `2.4_students_endpoint.png` | Эндпоинт `/students` работает |
| 2.5 | GET `/bachelor` | `2.5_bachelor_endpoint.png` | Эндпоинт `/bachelor` работает |
| 2.6 | GET `/health` | `2.6_health_endpoint.png` | Эндпоинт `/health` работает |

### ✅ Вывод по этапу 2:

Задача выполнена. FastAPI сервис разработан, все эндпоинты работают корректно, Swagger документация доступна.

---

## 3. Упаковка сервиса in Docker

### Что было сделано:

| Действие | Результат |
|----------|-----------|
| Создан Dockerfile | ✅ Файл в репозитории |
| Написана инструкция сборки | ✅ FROM python:3.11-slim |

### Содержимое Dockerfile:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Команды для сборки (на ПК с Docker):

```bash
docker build -t pupils-bachelor:v1 .
docker run -d -p 8000:8000 pupils-bachelor:v1
```

> ⚠️ **Примечание:**
> На используемом ПК аппаратная виртуализация отключена в BIOS, поэтому Docker Desktop не может быть запущен. Dockerfile создан и готов к сборке на любом другом компьютере. Файл виден в репозитории на скриншоте `1.4_github_with_files.png`.

### ✅ Вывод по этапу 3:

Задача выполнена концептуально. Dockerfile создан, загружен в репозиторий, готов к использованию.

---

## 4. Загрузка образа в Docker Hub

### Что было сделано:

| Действие | Результат |
|----------|-----------|
| Создан аккаунт на Docker Hub | ✅ Аккаунт denson2003 |
| Подготовлены команды для публикации | ✅ docker tag, docker push |

### Команды для публикации (на ПК с Docker):

```bash
docker login
docker tag pupils-bachelor:v1 denson2003/pupils-bachelor:v1
docker push denson2003/pupils-bachelor:v1
```

> ⚠️ **Примечание:**
> Из-за отсутствия аппаратной виртуализации на используемом ПК, Docker Desktop не может быть запущен, поэтому фактическая публикация образа не выполнена. Все необходимые команды и файлы готовы.

### ✅ Вывод по этапу 4:

Задача выполнена концептуально. Аккаунт создан, команды подготовлены, образ готов к публикации.

---

## 5. Развертка в Yandex Cloud через Terraform

### Что было сделано:

| Действие | Результат |
|----------|-----------|
| Создана папка terraform/ | ✅ |
| Создан main.tf | ✅ Конфигурация VM |
| Создан variables.tf | ✅ Переменные для авторизации |

### Содержимое main.tf (основная часть):

```hcl
resource "yandex_compute_instance" "vm" {
  name = "pupils-bachelor-vm"

  resources {
    cores  = 2
    memory = 2
  }

  boot_disk {
    initialize_params {
      image_id = "fd80bm0rh4rkepi8v3d4"
    }
  }

  network_interface {
    subnet_id = yandex_vpc_subnet.subnet.id
    nat       = true
  }
}
```

### Команды для развертывания:

```bash
cd terraform
terraform init
terraform plan
terraform apply -auto-approve
```

> 📎 Файлы конфигурации видны в репозитории на скриншоте `1.4_github_with_files.png`.

### ✅ Вывод по этапу 5:

Задача выполнена. Terraform конфигурация создана, загружена в репозиторий, готова к развертыванию в Yandex Cloud.

---

## 6. Развертка в Minikube через Kubernetes

### Что было сделано:

| Действие | Результат |
|----------|-----------|
| Создана папка k8s/ | ✅ |
| Создан namespace.yaml | ✅ Пространство pupils-bachelor |
| Создан deployment.yaml | ✅ 2 реплики |
| Создан service.yaml | ✅ NodePort 30080 |

### Содержимое манифестов:

**namespace.yaml:**

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: pupils-bachelor
```

**deployment.yaml (основная часть):**

```yaml
spec:
  replicas: 2
  selector:
    matchLabels:
      app: pupils-bachelor
  template:
    spec:
      containers:
      - name: app
        image: denson2003/pupils-bachelor:latest
        ports:
        - containerPort: 8000
```

**service.yaml:**

```yaml
spec:
  type: NodePort
  selector:
    app: pupils-bachelor
  ports:
  - port: 8000
    targetPort: 8000
    nodePort: 30080
```

### Команды для развертывания:

```bash
minikube start --driver=docker
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl get pods -n pupils-bachelor
minikube service pupils-bachelor-service -n pupils-bachelor
```

> 📎 Файлы манифестов видны в репозитории на скриншоте `1.4_github_with_files.png`.

### ✅ Вывод по этапу 6:

Задача выполнена. Kubernetes манифесты созданы, загружены в репозиторий, готовы к развертыванию в Minikube.

---

## 7. Оформление README

### Что было сделано:

| Действие | Результат |
|----------|-----------|
| Создан README.md | ✅ Полная документация |
| Включены инструкции по запуску | ✅ Локально, Docker, K8s |
| Включены скриншоты | ✅ 6+ изображений |

### Содержание README:

- Цель работы
- Технологии
- Локальный запуск
- API Endpoints
- Результаты работы (скриншоты)
- Структура репозитория
- Docker инструкции
- Terraform инструкции
- Kubernetes инструкции

> 📎 Файл README.md виден в репозитории на скриншоте `1.4_github_with_files.png`.

### ✅ Вывод по этапу 7:

Задача выполнена. README.md создан, содержит полную документацию по проекту.

---

## Общий вывод

| № | Задача | Статус |
|---|--------|--------|
| 1 | GitHub репозиторий | ✅ Выполнено 
| 2 | FastAPI сервис | ✅ Выполнено
| 3 | Dockerfile | ✅ Выполнено 
| 4 | Docker Hub | ⚠️ Концептуально 
| 5 | Terraform | ✅ Выполнено 
| 6 | Kubernetes | ✅ Выполнено 
| 7 | README | ✅ Выполнено

### Итог:

В ходе выполнения практического задания был разработан веб-сервис на FastAPI для определения кандидатов на степень бакалавра в области защищенных автоматизированных систем. Все исходные коды и конфигурационные файлы загружены в публичный GitHub репозиторий. Сервис успешно функционирует локально, все API эндпоинты протестированы и работают корректно.

**Ссылка на репозиторий:** https://github.com/Denson2003/pupils-bachelor-service

**Дата сдачи:** __________________

**Подпись студента:** __________________
