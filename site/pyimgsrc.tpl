<html>
  <head>
    <META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=utf-8">
    <title>py-imgsrc</title>
    <meta name="keywords" content="imgsrc, imgsrc.ru, client, imgsrc.ru client, linux, unix, freebsd, bsd">
  </head>
  <body>
	  <h1>релизы</h1>
	  %%CHANGELOG%%

	  <h1>установка</h1>
	  <p>Последняя версия доступна по адресу:
	  
	  <a href="http://people.freebsd.org/~novel/misc/pymgsrc-%%VERSION%%.tar.gz">http://people.freebsd.org/~novel/misc/pymgsrc-%%VERSION%%.tar.gz</a>. Также возможно воспользоваться git'ом:

          <pre>git clone git://github.com/novel/pymgsrc.git</pre>


	  Для работы требуется Python, я тестировал с 2.5, как работает с другими версиями - не знаю.

	  После скачивания необходимо распаковать архив (<i>tar zxvf pymgsrc-%%VERSION%%.tar.gz</i>) и
	  выполнить <i>sudo python setup.py install</i>.
	  </p>

	  <h1>использование</h1>
	  <p>Прежде всего, требуется записать свой логин и пароль от аккаунта на imgsrc.ru, сделать это
	  можно следующим образом (логин и пароль разделены двоеточием):<p>

	  <pre>echo login:password &gt; ~/.imgsrc</pre>

	  <h2>получение списка альбомов</h2>
	  <p>Для получения списка альбомов используется команда <i>lsalb</i>:</p>

	  <pre>%&gt; pymgsrc.py lsalb
123456 : some album (54; 2008-03-06 10:02:03)
123457 : really cool stuff (12; 2007-12-15 17:15:59)
	  </pre>

	  <ul>
	    <li>Первый столбец (123456, 123457) - номер альбома. Используется при добавлении фото в альбом.</li>
	    <li>Второй столбец (после двоеточия) - название альбома</li>
	    <li>Скобки: (количество_фото; дата_последнего_изменения)</li>
          </ul>

	  <h2>получение списка категорий</h2>
	  <p>Для получения списка категорий используется команда <i>lscat</i>:</p>

	  <pre>%&gt; pymgsrc.py lscat
+ 56 : HDR
+ 4 : авто-мото
  + 45 : accent-club
  + 57 : mazda3-club
.....
</pre>

	  <h2>создание альбома</h2>
	  <p>Для создания альбома используется команда <i>cralb</i>:</p>

	  <pre>%&gt; pymgsrc.py cralb 'my new cool album' 4</pre>

	  <p>Первый аргумент - название альбома, второй - численный номер категории (можно посмотреть весь
	  список категорий, воспользовавшись командой <i>lscat</i>, описанной выше.</p>

	  <h2>добавление фото в альбом</h2>
	  <p>Добавление фото в альбом осуществляется следующим образом:</p>

	  <pre>%&gt; pymgsrc.py 12345 ~/fotos/some_party/*.jpg http://my.friend.com/uploaded/some/photos/too.jpg</pre>

	  <p>Первый аргумент - id альбома, куда следует добавить фотографии. Остальные аргументы - либо
	  пути к файлам, либо URL'ы.</p>

	  <h1>todo / feedback</h1>
	  <p>С вопросами и пожеланиями в почту - novel2freebsd.org.</p>

	  <p>Создание запароленных альбомов не работает ввиду того, что эта функциональность мне лично
	  не нужна, я не создаю запароленных альбомов.</p>
  </body>
</html>
