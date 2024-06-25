# Script-pentru-testarea-unei-aplicatii
timp de execuție, input-output, apeluri de sistem(strace), apeluri de biblioteca(ltrace)

# 17.06.2024
Am studiat urmatoarele articole ce fac referire la framework-urile de testare a aplicatiilor
->https://www.codeproject.com/Articles/1156938/doctest-the-lightest-Cplusplus-unit-testing-framew
->https://ro.myservername.com/application-testing-into-basics-software-testing
->https://katalon.com/resources-center/blog/java-testing-frameworks
->https://www.selenium.dev/documentation/

# 18.06.2024
Am adaugat un test de verificare pentru o aplicatie. In el verific timpul de executie, apelurile de sistem, valoarea returnata de executia aplicatiei si rezultatul obtinut.

# 19.06.2024
Am implementat vizualizarea diferentelor dintre rezultatul dorit si cel obtinut, a fisierelor create, a apelurilor de biblioteca si a semnalelor transmise. Acestea functioneaza independent pentru fiecare test asupra codului daca acesta primeste input doar prin intermediul parametrilor. 

# 20.06.2024
Am finalizat scriptul pentru realizarea testelor, insa acesta functioneaza pe baza unui fisier de configuratie ce necesita o anumita forma specifica. Utilizatorul trebuie sa introduca in fisierul de configuratie calea catre aplicatie, fisierul ce contine argumentele necesare, fisierele de input si fisierul ce contine output-ul asteptat. 

# 21.06.2024
Am inceput sa lucrez la o interfata pentru script-ul creat in python qt.

# 24.06.2024
Am adaugat o interfata grafica pentru script astfel incat interactiunea utilizatorului cu mediul de testare sa fie mai usor de realizat. La deschiderea interfetei, utilizatorului ii va fi prezentata o fereastra in care va introduce calea catre aplicatie/fisierul executabil, o lista cu optiuni de afisare a detaliilor fiecarui test si un buton de adaugare a unui nou test care va deschide o noua fereastra cu trei campuri (argumente, input si expected output) ce vor fi completate in functie de necesitatile utilizatorului.
Dupa adaugarea acestor detalii de testare, se va incepe testarea prin apasarea butonului de start test care va rula scriptul de testare si va prelua informatiile oferite de acesta pentru a le afisa utilizatorului. 