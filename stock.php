<!DOCTYPE html>
<html>
<body>

<h1>Yahoo Stock DB</h1>


<?php

$servername = "localhost";
$username = "root";
$password = "snow5hite";

// Create connection
$conn = mysqli_connect ($servername, $username, $password, "CS288");


// Check connection
//if (!$conn){
//    echo ("Connection failed: " . mysqli_connect_error());
//}
//else {
//    echo "Connected successfully";
//}


// Save tablename to be fetched in MySQL
$table = "yahoo_2020_12_03_09_20_02";

// Print out the table name
echo "<h2><font color=\"green\">Table: " . $table . "</font></h2>\n";


// Fetch data from DB
$result = mysqli_query($conn, "SELECT * FROM $table");



// Save number of columns in a variable
$ncol = mysqli_num_fields($result);
//DEBUG
//echo ("Number of columns = $ncol");



// Set border attribute of table
$table_attrs = "border='1'";

// Create an HTML table
echo ("<table $table_attrs>");

// Fetch column names and insert into table
echo ("<tr>");
while ($field = mysqli_fetch_field($result)){
    $field_name = $field->name;
    echo ("<th>$field_name</th>");
}
echo ("</tr>");


// Fetch each row in DB table and insert into HTML table
while ($row = mysqli_fetch_array($result)){
    echo ("<tr>");
    for ($col=0 ; $col < $ncol ; $col++){
        echo ("<td>$row[$col]</td>");
    }
    echo ("</tr>");
}

// Finished creating table
echo ("</table>");



//echo ("<h3>Bello</h3>");

?>

</body>
</html>
