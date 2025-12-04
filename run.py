from app import create_app

app = create_app()

if __name__ == '__main__':
    # Добавляем сообщение для удобства
    print("\n" + "="*50)
    print("🚀  Сайт доступен по адресу: http://localhost:8000")
    print("="*50 + "\n")
    
    app.run(debug=True, host='0.0.0.0')