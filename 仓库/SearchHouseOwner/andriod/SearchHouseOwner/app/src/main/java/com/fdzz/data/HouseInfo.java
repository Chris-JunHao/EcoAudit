package com.fdzz.data;

import org.json.JSONObject;

/**
 * Created by yueguang on 16-1-26.
 */
public class HouseInfo {
    public String mId;
    public String mLocation;
    public String mCourt;
    public String mImage;
    public String mPhone;
    public String mPrice;

    public HouseInfo(JSONObject info) {
        mId = info.optString("objectId");
        mLocation = info.optString("weizhi");
        mCourt = info.optString("xiaoqu");
        mImage = info.optString("img");
        mPhone = info.optString("phone");
        mPrice = info.optString("price");
    }
}
