package com.fdzz.searchhouseowner;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.os.Handler;

import com.fdzz.common.CommonUtil;

public class WelcomeActivity extends BaseActivity {
    private static final String SP_NAME = "config";
    private static final String TAG_FIRST = "is_first_run";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_welcome);

        int mainColor = getResources().getColor(R.color.welcomeColor);
        CommonUtil.setStatusBarColor(this, mainColor);

        new Handler().postDelayed(new Runnable() {
            @Override
            public void run() {
                SharedPreferences sp = getSharedPreferences(SP_NAME, Context.MODE_PRIVATE);
                Intent activityIntent;
                if (sp.getBoolean(TAG_FIRST, true)) {
                    sp.edit().putBoolean(TAG_FIRST, false).apply();
                    activityIntent = new Intent(WelcomeActivity.this, ProtocolActivity.class);
                } else {
                    activityIntent = new Intent(WelcomeActivity.this, MainActivity.class);
                }
                startActivity(activityIntent);
                finish();
            }
        }, 1500);
    }
}
