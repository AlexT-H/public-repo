package edu.wgu.d387_sample_code.rest;

import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Date;
import java.util.ArrayList;
import java.util.TimeZone;
import java.util.List;
import java.text.SimpleDateFormat;

@RestController
@RequestMapping("/time")
@CrossOrigin
public class TimeController {

    final private String startTime = "08:00PM EST";
    final private String dateTimeFormat = "hh:mm";
    final private String[] timeZones = new String[]{"EST","MST","UTC"};
    private SimpleDateFormat timeFormater = new SimpleDateFormat(dateTimeFormat);

    @GetMapping("/presentation")
    public List<String> getTimes() {

        List<String> presentationTimes = new ArrayList<String>();

        try {
            Date date = timeFormater.parse(startTime);
            for (String t : timeZones) {
                TimeZone tz = TimeZone.getTimeZone(t);
                timeFormater.setTimeZone(tz);
                String dateOut = timeFormater.format(date);
                presentationTimes.add(dateOut);
            }
            TimeZone tzEST = TimeZone.getTimeZone("EST");
            timeFormater.setTimeZone(tzEST);
            TimeZone tzMST = TimeZone.getTimeZone("MST");
            TimeZone tzUTC = TimeZone.getTimeZone("UTC");
        } catch (Exception e) {
            System.out.println(e.toString());
        }

        return presentationTimes;

    }
}
