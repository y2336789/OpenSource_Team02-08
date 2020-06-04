import turtle
import random
import sqlite3
con = sqlite3.connect("C:/Users/영재/Desktop/opensourcequiz/testDB")    ## 파일 디렉토리는 바뀔 수 있다.
cur = con.cursor()
#cur.execute("DROP TABLE userTable") #2번 이상 실행될 경우 테이블을 삭제하고 다시 만든다.
cur.execute("CREATE TABLE userTable (Id char(4),R float(2),G float(2),B float(2),sequence char(4), xPos char(4), yPos char(4))")

## 전역 변수 선언 부분 ##
swidth, sheight, pSize, exitCount = 300, 300, 3, 0
r, g, b, angle, dist, curX, curY = [0] * 7
Db_r,Db_g,Db_b,Db_curX,Db_curY = [0] * 5
row = None

## 메인 코드 부분 ##
turtle.title('거북이가 맘대로 다니기')
turtle.shape('turtle')
turtle.pensize(pSize)
turtle.setup(width=swidth+30, height=sheight+30)
turtle.screensize(swidth, sheight)

seq = 1
data = ()
exitCount = 1
while True :
    r = random.random()
    g = random.random()
    b = random.random()
    turtle.pencolor((r, g, b))
    turtle.speed(5)
    
    angle =  random.randrange(0,360)
    dist = random.randrange(1,100)
    turtle.left(angle)
    turtle.forward(dist)
    curX = turtle.xcor()
    curY = turtle.ycor()

    if (-swidth / 2 <= curX and curX <= swidth / 2) and (-sheight / 2<= curY and curY <= sheight / 2) :
        #row = (exitCount,r,g,b,seq,curX,curY)
        row = (exitCount,round(r,2),round(g,2),round(b,2),seq,round(curX,2),round(curY,2))
        data += (row,) #경계선 바깥으로 나가기 전까지 이동한 행적을 한 행에 저장
        seq += 1
    else :
        turtle.penup()
        turtle.goto( 0, 0 )
        turtle.pendown()
        row = (exitCount,round(r,2),round(g,2),round(b,2),seq,round(curX,2),round(curY,2))
        data += (row,) #경계선 바깥으로 나갔을 때 마지막으로 데이터를 넣는다.
        seq=1        
        exitCount += 1
        if exitCount >= 6 :
            break


#cur.execute("INSERT INTO userTable VALUES('"+exitCount+"','"+r+"','"+g+"','"+b+"','"+seq+"','"+curX+"','"+curY+"')")
sql = "insert into userTable(Id,R,G,B,sequence,xPos,yPos) values (?, ?, ?, ?, ?, ?, ?)"
cur.executemany(sql, data) #데이터 한 번에 저장
con.commit() #DB에 저장

##거꾸로 그리기##
new_data = () #역순으로 저장될 데이터
for i in reversed(range(len(data))):
    new_data += (data[i],) #데이터를 역순으로 저장
index=0
Max=0
loop=0
turtle.clear()
turtle.penup()
turtle.goto(new_data[0][5],new_data[0][6])
num = exitCount-1
for i in range(--num):
    turtle.speed(5)
    Max += new_data[index][4] #한 행에서 최대 순번
    for loop in range(index,Max): #그리기
        if loop==index: #처음엔 좌표로 이동만 한다.
            curX = new_data[loop][5]
            curY = new_data[loop][6]
            turtle.penup()
            turtle.goto( curX, curY )
            continue
        else: #그릴 때는 pencolor를 이전에 저장되어있는 색상 값으로 설정한다.
            r = new_data[loop-1][1]
            g = new_data[loop-1][2]
            b = new_data[loop-1][3]
            turtle.pencolor((r, g, b))
            turtle.pendown()
            curX = new_data[loop][5]
            curY = new_data[loop][6]
            turtle.goto( curX, curY ) #그린다.
            turtle.penup()

    r = new_data[Max-1][1]
    g = new_data[Max-1][2]
    b = new_data[Max-1][3]
    turtle.pencolor((r, g, b))
    turtle.pendown()
    turtle.goto(0,0) #마지막에 원점으로 이동하면서 색칠한다.
    turtle.penup()
    index = Max


con.close() #DB닫기
turtle.done()
