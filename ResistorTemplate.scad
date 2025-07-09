module resistor(leg_width,leg_height, resistor_width,resistor_lenght,distance_between_legs)

{
    
    
    cylinder(h=leg_height, d = leg_width, $fn = 100);
    
    translate([distance_between_legs, 0, 0])
    cylinder(h=leg_height, d = leg_width, $fn = 100);
    
    translate([0,0,leg_height])
    rotate([0,90,0])
    cylinder(h=distance_between_legs, d = leg_width,$fn = 100);
    
    translate([0,0,leg_height])
    sphere(d=leg_width,$fn = 100);
    
    translate([distance_between_legs,0,leg_height])
    sphere(d=leg_width,$fn = 100);
    
    
    translate([((distance_between_legs-resistor_lenght)/2),0,leg_height])
    rotate([0,90,0])
    cylinder(h=resistor_lenght, d = resistor_width,$fn = 100);
    
};





resistor(leg_width = 0.5,
    leg_height = 15,
    
    resistor_width = 3,
    resistor_lenght = 8.5,
    
    distance_between_legs = 12.7);
