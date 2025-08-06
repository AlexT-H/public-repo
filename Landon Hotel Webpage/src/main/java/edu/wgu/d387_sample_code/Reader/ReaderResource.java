package edu.wgu.d387_sample_code.Reader;

import java.util.Locale;
import java.util.ResourceBundle;

public class ReaderResource {
    private Locale var;
    private ResourceBundle resBundle;

    public String getMsg() {
        return resBundle.getString("welcome");
    }

    public ReaderResource() {

    }

    public ReaderResource(String lang, String country){
        var = new Locale(lang,country);
        System.out.println("rr here");
        resBundle = ResourceBundle.getBundle("translation",var);
    }

}
