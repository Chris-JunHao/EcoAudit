package com.fdzz.searchhouseowner;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;

/**
 * Created by yueguang on 16-1-29.
 */
public class ProtocolActivity extends BaseActivity implements View.OnClickListener {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_protocol);
        findViewById(R.id.ok).setOnClickListener(this);
    }

    @Override
    public void onClick(View view) {
        Intent activityIntent = new Intent(ProtocolActivity.this, MainActivity.class);
        startActivity(activityIntent);
        finish();
    }
}
