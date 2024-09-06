package com.fdzz.searchhouseowner;

import android.app.Activity;
import android.app.ProgressDialog;

import com.umeng.analytics.MobclickAgent;

/**
 * Created by yueguang on 16-1-29.
 */
public class BaseActivity extends Activity {
    private ProgressDialog mProgressDialog;

    @Override
    public void onResume() {
        super.onResume();
        MobclickAgent.onResume(this);
    }

    @Override
    public void onPause() {
        super.onPause();
        MobclickAgent.onPause(this);
    }

    protected void showProgressDialog() {
        mProgressDialog = new ProgressDialog(this);
        mProgressDialog.setMessage(getString(R.string.loading));
        mProgressDialog.show();
    }

    protected void dismissProgressDialog() {
        if (mProgressDialog != null) {
            mProgressDialog.dismiss();
        }
    }
}
