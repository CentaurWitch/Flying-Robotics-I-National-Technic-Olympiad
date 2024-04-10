Rectify_Point and Solfpnp. Программирование квадрокоптера COEX Clover. Программа red_circle.py.
-

Часть кода red_circle.py, содержащая библиотеку OPENCV, для обработки изображений с камеры дрона.
-

<details>
      <summary>Фотография части кода</summary>
      <img width="672" alt="image" src="https://github.com/CentaurWitch/Flying-Robotics-I-National-Technic-Olympiad/assets/149146826/dae1d4dd-e078-406a-a901-90cd8da8aad9">

</details>

Рассмотрим код подробнее:
<details>
      <summary>Часть кода</summary>
      
      img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

      В данной части видно, что переменная img_hsv равна преобразованию переменной img в HSV-диапозон, за что и отвечает функция cv2.COLOR_BGR2HSV
</details>

<details>
      <summary>Часть кода</summary>
      
      mask1 = cv2.inRange(img_hsv, (0, 150, 150), (15, 255, 255))
      mask2 = cv2.inRange(img_hsv, (160, 150, 150), (180, 255, 255))
      # combine two masks using bitwise OR
      mask = cv2.bitwise_or(mask1, mask2)

      Функция cv2.inRange отвечает за диапозон цвета в HSV-диапазоне, т.к. используется переменная img_hsv
      Функция cv2.bitwise_or() служит для объединения двух диапозонов в один, с последующем выбором, к какому точно диапазону относится
</details>
