package com.example.plantsystem;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.NotificationCompat;

import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.util.Log;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.view.View;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;



public class MainActivity extends AppCompatActivity {

    public FirebaseDatabase database;
    public DatabaseReference myRef;

    TextView emotionTxtView;
    TextView moistureTxtView;
    TextView tempTxtView;
    TextView wateringEveryTxtView;
    TextView countdownTxtView;
    ImageView happyFace;
    Button waterButton;



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        //database = FirebaseDatabase.getInstance();
        readDatabase();



    }


    public void readDatabase() {
        FirebaseDatabase database = FirebaseDatabase.getInstance();
        final DatabaseReference myRef = database.getReference().child("MainUser"); //this is "plantsystem-1e4fa". "MainUser" adds branch


        // Read from the database
        myRef.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                //For "Emotion"
                String value = dataSnapshot.child("Emotion").getValue(String.class); //MUST BE dataSnapshot.child().getValue()
                emotionTxtView = findViewById(R.id.emotionTxtView);
                emotionTxtView.setText(value);
                //determine imageView
                happyOrSad(emotionTxtView.getText().toString());//shows face for a second then disappears
                Log.d("d", "Value is: " + value);

                //For "Moisture"
                Integer moistureValue = dataSnapshot.child("Moisture").getValue(Integer.class);
                moistureTxtView = findViewById(R.id.moistureTxtView);
                moistureTxtView.setText(String.valueOf(moistureValue));
                Log.d("d", "Value is: " + moistureValue);

                //For "Temperature"
                Integer tempValue = dataSnapshot.child("Temperature").getValue(Integer.class);
                tempTxtView = findViewById(R.id.tempTxtView);
                tempTxtView.setText(String.valueOf(tempValue));
                Log.d("d", "Value is: " + tempValue);

                //For "HoursBetweenWatering"
                Integer hoursValue = dataSnapshot.child("SetHoursBetweenWatering").getValue(Integer.class);
                wateringEveryTxtView = findViewById(R.id.wateringEveryTxtView);
                wateringEveryTxtView.setText("Every " + String.valueOf(hoursValue) + " hours");
                Log.d("d", "Value is: " + hoursValue);

                //For "Countdown"
                Integer countValue = dataSnapshot.child("Countdown").getValue(Integer.class);
                countdownTxtView = findViewById(R.id.countdownTxtView);
                countdownTxtView.setText(String.valueOf(countValue));
                Log.d("d", "Value is: " + countValue);
            }

            @Override
            public void onCancelled(DatabaseError error) {
                // Failed to read value
                Log.w("d", "Failed to read value.", error.toException());
            }
        });

        waterButton = findViewById(R.id.waterButton);
        waterButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                //Activate motor
                myRef.child("ButtonPressed").setValue(1);
                Log.i("MOTOR: ","Motor turned on");

            }
        });
    }


    //NOT SWITCHING FACES
    public void happyOrSad(final String emo) {
        happyFace = findViewById(R.id.happyFace);
        if (emo.equals("Happy")) {
            happyFace.setImageDrawable(getResources().getDrawable(R.drawable.happyface, getApplicationContext().getTheme()));
        } else if (emo.equals("Sad")) {
            happyFace.setImageDrawable(getResources().getDrawable(R.drawable.sadface, getApplicationContext().getTheme()));

        }

    }



}











