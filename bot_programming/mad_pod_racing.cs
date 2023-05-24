// this is bugged atm

using System;
using System.Linq;
using System.IO;
using System.Text;
using System.Collections;
using System.Collections.Generic;

/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/

class Point {
    public int x;
    public int y;
    public Point(int x, int y){
        this.x = x;
        this.y = y;
    }
}



class Player
{
    static void Main(string[] args)
    {
        string[] inputs;
        bool boostUsed = false;
        List<Point> checkpoints = new List<Point>();
        bool roundOne = true;


        // game loop
        while (true)
        {
            inputs = Console.ReadLine().Split(' ');
            int x = int.Parse(inputs[0]);
            int y = int.Parse(inputs[1]);
            int nextCheckpointX = int.Parse(inputs[2]); // x position of the next check point
            int nextCheckpointY = int.Parse(inputs[3]); // y position of the next check point

            int nextCheckpointDist = int.Parse(inputs[4]); // distance to the next checkpoint
            int nextCheckpointAngle = int.Parse(inputs[5]); // angle between your pod orientation and the direction of the next checkpoint
            inputs = Console.ReadLine().Split(' ');
            int opponentX = int.Parse(inputs[0]);
            int opponentY = int.Parse(inputs[1]);
            int thrust = 0;

            Point nextPoint = GetNextPoint(nextCheckpointDist, nextCheckpointAngle);
            nextCheckpointX = nextPoint.x;
            nextCheckpointY = nextPoint.y;


            bool angleForBoost = (nextCheckpointAngle < 5 && nextCheckpointAngle > -5);
            if (angleForBoost && !boostUsed) {
                if (roundOne){
                    Console.WriteLine(nextCheckpointX + " " + nextCheckpointY + " BOOST");
                    boostUsed = true;
                    roundOne = false;
                    continue;
                }
                if (nextCheckpointDist > 7000 ) {   
                    Console.WriteLine(nextCheckpointX + " " + nextCheckpointY + " BOOST");
                    boostUsed = true;
                    continue;
                }
            }
            
            if (nextCheckpointAngle > 90 || nextCheckpointAngle < -90){
                thrust = 0;
            } else {
                thrust = 100;
            }
            bool  angleForSpeed = (nextCheckpointAngle < 5 && nextCheckpointAngle > -5);
            if (nextCheckpointDist < 600 && angleForSpeed){
                thrust = 0;
                Console.WriteLine(nextCheckpointX + " " + nextCheckpointY + " " + thrust);       
            } else if (nextCheckpointDist < 1000 && angleForSpeed) {
                thrust = 10;
                Console.WriteLine(nextCheckpointX + " " + nextCheckpointY + " " + thrust);       
            } else if (nextCheckpointDist < 1500 && angleForSpeed) {
                thrust = 15;
                Console.WriteLine(nextCheckpointX + " " + nextCheckpointY + " " + thrust);       
            } else {
                Console.WriteLine(nextCheckpointX + " " + nextCheckpointY + " " + thrust); 
            }
            bool enemyClose = EnemyIsClose(x, y, opponentX, opponentY);
            if (enemyClose) {
                Console.Error.WriteLine("Shield used");
                Console.WriteLine(nextCheckpointX + " " + nextCheckpointY + " SHIELD");
            }
            roundOne = false;
        }
    }

    private static Point GetNextPoint(int nextCheckpointDist, int nextCheckpointAngle){
        int newDistance = nextCheckpointDist ;
        double new_y = newDistance * Math.Sin(Math.Abs(nextCheckpointAngle));
        double new_x = newDistance * Math.Cos(Math.Abs(nextCheckpointAngle));
        return new Point(Convert.ToInt32(new_x), Convert.ToInt32(new_y));
    }

    private static bool EnemyIsClose(int my_x, int my_y, int enemy_x, int enemy_y){
        int distanceToEnemy = 801;
        distanceToEnemy = DistanceToEnemy(my_x, my_y, enemy_x, enemy_y);
        return distanceToEnemy < 800;
    }
    private static int DistanceToEnemy(int my_x, int my_y, int enemy_x, int enemy_y){
        return Convert.ToInt32(Math.Sqrt(Math.Abs(my_x - enemy_x) * Math.Abs(my_x-enemy_x) + Math.Abs(my_y - enemy_y) * Math.Abs(my_y-enemy_y)));
    }
}