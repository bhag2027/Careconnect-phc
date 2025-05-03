package com.example.trufbooking;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.RatingBar;
import android.widget.Toast;

import org.json.JSONObject;

public class Review extends AppCompatActivity implements JsonResponse {
    RatingBar ratingBar;
    Button getRating;
    SharedPreferences sh;
    Float rated;
    EditText e1;
    String rat,review,rv;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_review);
        getRating = (Button) findViewById(R.id.getRating);
        ratingBar = (RatingBar) findViewById(R.id.rating);

        e1=(EditText)findViewById(R.id.etreview);

        sh= PreferenceManager.getDefaultSharedPreferences(getApplicationContext());


        JsonReq JR=new JsonReq();
        JR.json_response=(JsonResponse)Review.this;
        String q = "/ViewReview?turf_id="+ViewTurf.turf_ids+"&login_id="+Login.logid;
        q=q.replace(" ", "%20");
        JR.execute(q);

        getRating.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                float rating =  ratingBar.getRating();
                review=e1.getText().toString();

                JsonReq JR=new JsonReq();
                JR.json_response=(JsonResponse)Review.this;
                String q = "/Review?turf_id="+ViewTurf.turf_ids+"&rating="+rating+"&review="+review+"&login_id="+Login.logid;
                JR.execute(q);
                Log.d("pearl",q);
            }
        });
    }



    public void response(JSONObject jo) {
        // TODO Auto-generated method stub


        try {
            String method=jo.getString("method");
            if(method.equalsIgnoreCase("ViewReview"))
            {
                try{
                    Toast.makeText(getApplicationContext(),"helloooooooo", Toast.LENGTH_SHORT).show();
                    String status=jo.getString("status");
                    Log.d("result", status);

                    if(status.equalsIgnoreCase("success")){

                        rat=jo.getString("data");
                        rated=Float.parseFloat(rat);
                        e1.setText(jo.getString("data1"));
                        Toast.makeText(getApplicationContext(),rated+"", Toast.LENGTH_SHORT).show();
                        ratingBar.setRating(rated);



                    }
                    else
                    {
                        Toast.makeText(getApplicationContext(), "no data", Toast.LENGTH_LONG).show();
                    }

                }catch(Exception e)
                {
                    Toast.makeText(getApplicationContext(), e.toString(), Toast.LENGTH_LONG).show();
                }
            }else if(method.equalsIgnoreCase("user_review_comapny"))
            {
                try {
                    String status=jo.getString("status");
                    if(status.equalsIgnoreCase("success"))
                    {
                        Toast.makeText(getApplicationContext()," Added success", Toast.LENGTH_LONG).show();
                        startActivity(new Intent(getApplicationContext(),Review.class));
                    }
                    else
                    {
                        Toast.makeText(getApplicationContext(), "Rating failed",Toast.LENGTH_LONG ).show();
                    }
                } catch (Exception e){
                    // TODO: handle exception
                }
            }

        }

        catch(Exception e)
        {
            Toast.makeText(getApplicationContext(), e.toString(), Toast.LENGTH_LONG).show();
        }

    }




    public void onBackPressed()
    {
        // TODO Auto-generated method stub
        super.onBackPressed();
        Intent b=new Intent(getApplicationContext(),ViewTurf.class);
        startActivity(b);
    }

}