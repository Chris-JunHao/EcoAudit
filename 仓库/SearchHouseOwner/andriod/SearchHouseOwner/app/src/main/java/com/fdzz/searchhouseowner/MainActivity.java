package com.fdzz.searchhouseowner;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

import com.fdzz.common.CommonDefine;
import com.fdzz.common.CommonUtil;
import com.loopj.android.http.AsyncHttpClient;
import com.loopj.android.http.RequestParams;
import com.loopj.android.http.TextHttpResponseHandler;

import org.apache.http.Header;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * 主界面
 * Created by yueguang on 16-1-25.
 */
public class MainActivity extends BaseActivity implements View.OnClickListener {
    public static final String RESULT = "result";
    public static final String PHONE = "phone";
    private EditText mPhone;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        int mainColor = getResources().getColor(R.color.mainColor);
        CommonUtil.setStatusBarColor(this, mainColor);

        mPhone = (EditText) findViewById(R.id.phone);
        findViewById(R.id.check).setOnClickListener(this);

        findViewById(R.id.part).setOnClickListener(this);
        findViewById(R.id.all).setOnClickListener(this);
        findViewById(R.id.owner).setOnClickListener(this);
    }

    @Override
    public void onClick(View view) {
        switch (view.getId()) {
            case R.id.check:
                final String phone = mPhone.getText().toString();
                if (isPhoneOk(phone)) {
                    showProgressDialog();
                    AsyncHttpClient asyncHttpClient = new AsyncHttpClient();
                    RequestParams rp = new RequestParams();
                    rp.add("phone", phone);
                    asyncHttpClient.get(CommonDefine.SERVER + CommonDefine.CHECK_AGENT, rp, new TextHttpResponseHandler() {
                        @Override
                        public void onStart() {
                            super.onStart();
                        }

                        @Override
                        public void onFailure(int i, Header[] headers, String s, Throwable throwable) {
                            Log.e("xxxxx", "statusCode:" + i + "throwable:" + throwable);
                            Toast.makeText(MainActivity.this, R.string.net_err, Toast.LENGTH_SHORT).show();
                        }

                        @Override
                        public void onSuccess(int i, Header[] headers, String s) {
                            Log.i("xxxxx", "s:" + s);
                            Intent result = new Intent(MainActivity.this, ResultActivity.class);
                            result.putExtra(RESULT, s);
                            result.putExtra(PHONE, phone);
                            startActivity(result);
                        }

                        @Override
                        public void onFinish() {
                            super.onFinish();
                            dismissProgressDialog();
                        }

                    });
                } else {
                    Toast.makeText(this, R.string.phone_err, Toast.LENGTH_SHORT).show();
                }
                break;
            default:
                Toast.makeText(this, R.string.future_can_not_used, Toast.LENGTH_SHORT).show();
                break;
        }
    }

    private boolean isPhoneOk(String phone) {
        Pattern p = Pattern.compile("^((13[0-9])|(15[^4,\\D])|(18[0,2-9])|(17[0,5-9]))\\d{8}$");
        Matcher m = p.matcher(phone);
        return m.matches();
    }
}
